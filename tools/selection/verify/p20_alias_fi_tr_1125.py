"""Patch 20 (11-25): two books were listed twice because the selection title and the app title differ. Finland
"True (Totta)" is the app's book "True" (true-totta), and Turkey "Aşk-ı Memnu" is the app's "Forbidden Love"
(ask-i-memnu); both are already in the app. existing_alias matches them, so each shows once, as in the app.
Run in tools/selection: python3 -I verify/p20_alias_fi_tr_1125.py, then make_existing.py and build all."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import specio
for cc, title, bid in [("fi", "True (Totta)", "true-totta"), ("tr", "Aşk-ı Memnu", "ask-i-memnu")]:
    S = specio.load(cc)
    S.setdefault("existing_alias", {})[title] = bid
    specio.save(cc, S)
print("ok")
