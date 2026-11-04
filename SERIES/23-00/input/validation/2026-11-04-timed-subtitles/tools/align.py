#!/usr/bin/env python3
"""Align approved lyric lines to Whisper word times (timing evidence only).

The approved lyric text is never changed.  ASR text is used only to place the
approved lines on the time axis.  Semi-global monotone alignment on syllable
characters (Hangul syllables compared at jamo level), then per-line first/last
matched-character times.
"""
import json
import re
import unicodedata
from pathlib import Path

CHO = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"


def decompose(ch):
    o = ord(ch)
    if 0xAC00 <= o <= 0xD7A3:
        o -= 0xAC00
        return (o // 588, (o % 588) // 28, o % 28)
    return None


def norm_chars(text):
    """Characters kept for alignment: Hangul syllables, digits, Latin letters."""
    out = []
    for ch in unicodedata.normalize("NFC", text):
        if 0xAC00 <= ord(ch) <= 0xD7A3 or ch.isdigit():
            out.append(ch)
        elif ch.isalpha() and ord(ch) < 0x250:
            out.append(ch.lower())
    return out


def sim(a, b):
    if a == b:
        return 3.0
    da, db = decompose(a), decompose(b)
    if da and db:
        if da[0] == db[0] and da[1] == db[1]:
            return 1.5
        if da[1] == db[1] and da[2] == db[2] and da[2] != 0:
            return 1.0
        if da[0] == db[0] and da[2] == db[2] and da[2] != 0:
            return 0.5
    return -2.0


GAP_LYRIC = -1.0   # approved char not matched by ASR (unsung / missed)
GAP_ASR = -0.6     # ASR char with no approved char (hallucination, extra repeat)


def asr_chars(asr_json, offset_ms=0):
    """Return list of (char, start_s, end_s, word_index) from retained word timing."""
    words = [w for seg in asr_json["transcription"]["segments"] for w in seg.get("words", [])]
    out = []
    for wi, w in enumerate(words):
        chars = norm_chars(w["word"])
        if not chars:
            continue
        s, e = float(w["start"]), float(w["end"])
        n = len(chars)
        for k, ch in enumerate(chars):
            out.append((ch, s + (e - s) * k / n, s + (e - s) * (k + 1) / n, wi))
    return out, words


def align(lyric_chars, asr):
    """lyric_chars: list of (char, line_no). asr: list from asr_chars.  Returns match list."""
    n, m = len(lyric_chars), len(asr)
    NEG = -1e9
    dp = [[NEG] * (m + 1) for _ in range(n + 1)]
    bt = [[0] * (m + 1) for _ in range(n + 1)]  # 1 diag, 2 skip lyric (i-1), 3 skip asr (j-1), 4 free lead
    for j in range(m + 1):
        dp[0][j] = 0.0
        bt[0][j] = 4
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + GAP_LYRIC
        bt[i][0] = 2
        ci = lyric_chars[i - 1][0]
        row, prow = dp[i], dp[i - 1]
        for j in range(1, m + 1):
            best, how = prow[j - 1] + sim(ci, asr[j - 1][0]), 1
            v = prow[j] + GAP_LYRIC
            if v > best:
                best, how = v, 2
            v = row[j - 1] + GAP_ASR
            if v > best:
                best, how = v, 3
            row[j], bt[i][j] = best, how
    # free trailing ASR
    j = max(range(m + 1), key=lambda jj: dp[n][jj])
    i = n
    matches = []
    while i > 0:
        how = bt[i][j]
        if how == 1:
            s = sim(lyric_chars[i - 1][0], asr[j - 1][0])
            matches.append((i - 1, j - 1, s))
            i -= 1
            j -= 1
        elif how == 2:
            i -= 1
        elif how == 3:
            j -= 1
        else:
            break
    matches.reverse()
    return matches
