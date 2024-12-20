from flask import Flask, request, render_template, make_response
import os

from backend import (
    get_nouns_to_test,
    get_verb_to_test,
    get_words_to_test,
    check_noun,
    check_verb,
    check_vocab,
)


app = Flask(__name__)
N = 4


def check_cookies_allowed():
    cookies_allowed = request.cookies.get("cookies_allowed", "F")
    return cookies_allowed == "T"


@app.route("/cookies.html", methods=["POST", "GET"])
def ask_for_cookies():
    if request.method == "POST" and "allow" in request.form:
        response = make_response(render_template("index.html"))
        response.set_cookie("cookies_allowed", "T")
        return response
    cookie_fields = request.cookies.keys()
    response = make_response(render_template("cookies.html"))
    if request.method == "POST" and "clear" in request.form:
        for field in cookie_fields:
            response.set_cookie(field, "", expires=0)
    return response


@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def index():
    if not check_cookies_allowed():
        return ask_for_cookies()
    return render_template("index.html")


@app.route("/conjugate.html", methods=["GET"])
def conjugate():
    if not check_cookies_allowed():
        return ask_for_cookies()
    verb, meaning = get_verb_to_test()
    return render_template("verb_index.html", verb=verb, meaning=meaning)


@app.route("/derdiedas.html", methods=["GET"])
def derdiedas():
    if not check_cookies_allowed():
        return ask_for_cookies()
    nouns_to_test = get_nouns_to_test(N)
    return render_template("noun_index.html", words=nouns_to_test)


@app.route("/matchnouns.html", methods=["GET", "POST"])
def match_nouns():
    return vocabulary("nouns")


@app.route("/matchverbs.html", methods=["GET", "POST"])
def match_verbs():
    return vocabulary("verbs")


@app.route("/matchvocab.html", methods=["GET", "POST"])
def match_words():
    return vocabulary("vocab")


def vocabulary(style):
    if not check_cookies_allowed():
        return ask_for_cookies()

    def encode_array(arr):
        return "|".join(arr)

    def decode_array(arr):
        return arr.split("|")

    if request.method == "POST" and "check" in request.form:
        return vocab_check(style)

    if request.method == "POST" and "reset" in request.form:
        cookies = {}
    elif request.cookies.get("style") != style:
        cookies = {}
    else:
        cookies = request.cookies

    assert check_cookies_allowed()
    cookie_words = cookies.get("words", "")
    if "|" in cookie_words:
        words = decode_array(cookies.get("words"))
        meanings = decode_array(cookies.get("meanings"))
        assert len(words) == len(meanings)
    else:
        words, meanings = get_words_to_test(style, N)
    input_meanings = decode_array(cookies.get("input_meanings", encode_array([""] * N)))
    is_used = decode_array(cookies.get("is_used", encode_array(["F"] * N)))
    num_filled = int(cookies.get("num_filled", "0"))
    for i in range(N):
        if f"meaning_{i+1}" in request.form:
            if is_used[i] != "T":
                input_meanings[num_filled] = meanings[i]
                is_used[i] = "T"
                num_filled += 1
    if "revert" in request.form:
        if num_filled > 0:
            for i in range(N):
                if input_meanings[num_filled - 1] == meanings[i]:
                    is_used[i] = "F"
                    num_filled -= 1
                    input_meanings[num_filled] = ""
                    break
    response = make_response(
        render_template(
            "vocab_index.html",
            style=style,
            words=words,
            meanings=meanings,
            input_meanings=input_meanings,
            is_used=is_used,
            num_filled=num_filled,
        )
    )
    response.set_cookie("style", style)
    response.set_cookie("words", encode_array(words))
    response.set_cookie("meanings", encode_array(meanings))
    response.set_cookie("input_meanings", encode_array(input_meanings))
    response.set_cookie("is_used", encode_array(is_used))
    response.set_cookie("num_filled", str(num_filled))
    return response


@app.route("/noun_check.html", methods=["GET"])
def noun_check():
    outputs = check_noun(request.args, N)
    return render_template("noun_check.html", outputs=outputs)


@app.route("/verb_check.html", methods=["GET"])
def verb_check():
    outputs = check_verb(request.args)
    return render_template("verb_check.html", **outputs)


@app.route("/vocab_check_noun.html", methods=["POST"])
def vocab_check_noun():
    return vocab_check("nouns")


@app.route("/vocab_check_verb.html", methods=["POST"])
def vocab_check_verb():
    return vocab_check("verbs")


@app.route("/vocab_check_vocab.html", methods=["POST"])
def vocab_check_word():
    return vocab_check("vocab")


def vocab_check(style):
    outputs = check_vocab(request.form, style, N)
    response = make_response(
        render_template("vocab_check.html", style=style, outputs=outputs)
    )
    assert check_cookies_allowed()
    for cookie in request.cookies:
        response.set_cookie(cookie, "", expires=0)
    return response


if __name__ == "__main__":
    # this port needs to be exposed in the Dockerfile
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
