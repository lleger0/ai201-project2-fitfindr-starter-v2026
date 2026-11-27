# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

This is fitfinder, an agent that can search listings, suggest outfits, and create post ideas for it. The user can input an item description and based on that search for listings that matches that item. After that the agent will give two outfit ideas based on the users existing wardbrobe. The agent can then share a sample post caption, fully giving the user a full view of what it's like to have that listing item.



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** It searches the listings for items matching the description, and potentially the size and items with a price less than the maximum price. This tool does not call the AI model.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" --> This is a function that takes in a description (string), size (string), and maximum price (float).
- **Returns:** Returns items that match the parameters. Size and items less than the max price aren't strictly required.
- **When it has nothing:**  When this function has nothing to give it will return an empty list.

### `suggest_outfit`

- **What it does:**      This function calls the model through generate() and suggests a one or two outfits.

- **Inputs:** This function takes in a dictionary called new_item and a dictionary called wardrobe. The new_item is an item that the user is considering adding to their wardrobe. 
- **Returns:** This function returns a string with outfit suggestions. 
- **When it has nothing:**  If the wardrobe is empty, it will return general styling ideas for the new item.


### `create_fit_card`

- **What it does:** This function calls the model and writes a short caption that a person would post about the outfit.
- **Inputs:** It takes in 2 parameters: the outfit which is a string and new_item which is a dictionary. Outfit is a string from suggest_outfit().
- **Returns:** This function returns a two to four sentence caption.
- **When it has nothing:** If outfit is empty or whitespace it returns a descriptive message.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

<!-- **Branch rule:** If search_listings returns an empty list, put a message in the session and stop. Otherwise, take the first result and go to suggest_outfit -->

**Branch rule:** If search_listings returns an empty list, put a message in
        session["error"] naming what the user could change, and return the
        session without calling suggest_outfit. Otherwise take the first
        result, put it in session["selected_item"], and continue.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which --> The query is parsed into a dictionary that takes the description, size, and max_price from the query.  

**What moves through the session:** <!-- which fields, in what order -->
A list of items that match the query. Then one item is chosen. That item then moves through the rest of the session. The item has fields such as title, price, and platform. 

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
ex: $ python app.py ask '...'
$ python app.py ask 'vintage graphic tee under $30'

```
Result:

[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 8 items: Graphic Tee — 2003 Tour Bootleg Style, Y2K Baby Tee — Butterfly Print, Vintage Graphic Hoodie — Faded Black … +5 more
      →    8 match(es)
[3] select_item
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[4] suggest_outfit
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: Outfit 1: Pair the Graphic Tee — 2003 Tour Bootleg Style with your Baggy straight-leg jeans, dark wash, and fi…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: Score this 2003 tour bootleg style tee on depop for just $24. It has the ultimate faded grunge look that goes …

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Outfit 1:
Pair the Graphic Tee — 2003 Tour Bootleg Style with your Baggy straight-leg jeans, dark wash, and finish with your Black combat boots and Black crossbody bag. 
Why it works: This leans into an effortless, authentic 90s grunge look. The dark wash denim anchors the loud graphic, and the combat boots add that classic edgy finish.

Outfit 2:
Layer your Vintage black denim jacket over the Graphic Tee — 2003 Tour Bootleg Style, paired with your Wide-leg khaki trousers, and step into your Chunky white sneakers.
Why it works: It balances the dark, edgy streetwear vibe of the tee with the clean, relaxed earth tones of the khakis, while the cropped jacket pulls in your waist.

  Fit card: Score this 2003 tour bootleg style tee on depop for just $24. It has the ultimate faded grunge look that goes with everything in my closet. I’m living in this shirt all fall.

0 model calls this session, 2 served from cache

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
Output: 

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```
ex: $ python -c "from tools import suggest_outfit; ..."

$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

```
Output:

**Outfit 1: Effortless Streetwear**
Pair the Vintage Levi's 501 Jeans with the White ribbed tank top tucked in, layered under the Oversized grey crewneck sweatshirt, and finish with the Chunky white sneakers. 
*Why it works:* The fitted white tank balances the super-roomy grey crewneck, and the whole look leans into an easy, classic casual vibe anchored by those perfect vintage jeans.

**Outfit 2: Edgy Casual**
Wear the Vintage Levi's 501 Jeans with the Black cropped zip hoodie, the Vintage black denim jacket on top, and the Black combat boots. 
*Why it works:* Doubling up on black outerwear creates a cool, moody contrast against the medium-wash denim, and the combat boots give the straight-leg cut a tough, grounded finish.

```
example: $ python -c "from tools import create_fit_card; ..."

$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

```
Output:

Finally caved and grabbed these vintage Levi's 501s on Depop for $38 and I am never taking them off. Paired them with crisp white sneakers for that effortlessly cool 90s streetwear vibe. Honestly the medium wash denim fit is so unreal.

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1** 

- *What I asked for:* Assistance in writing the code for the suggest_outfit tool
- *What came back:* suggest_outfit() including the steps listed in the instructions
- *What I changed:* I implemented this as part of my code ensuring that it worked and passed all tests.

**Moment 2** 

- *What I asked for:* Assistance in writing the code for the create_fit_card tool
- *What came back:* create_fit_card() including the steps listed in the instructions
- *What I changed:* I implemented this as part of my code ensuring that it worked and passed all tests.


**Moment 3**


- *What I asked for:*  I asked the AI to ensure that all the requirements for Milestone 5 were met.
- *What came back:* The AI actually pointed out that my search_lisitngs tool was not sorting the listings properly.
- *What I changed:*  Using it's feedback, I was able to manually fix the code causing the issue. 


<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

<!-- | Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  | -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5)|
| 3. Item in session matches item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5)|
| 4. Fit card mentions the item's description | 3 of 5 | FAIL | PASS | PASS | PASS | PASS | MET (4/5) |
| 5. Over-budget query returns nothing over the limit | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5)  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

file: results\run_2026-11-26_2033_before.md

```
Cache is OFF for this run — that's deliberate.

matching query completes  (example wardrobe)
  query: vintage graphic tee under $30
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 8 items: Graphic Tee — 2003 Tour Bootleg Style, Y2K Baby Tee — Butterfly Print, Vintage Graphic Hoodie — Faded Black … +5 more
      →    8 match(es)
[3] select_item
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[4] suggest_outfit
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: Outfit 1: Pair your new graphic tee with the baggy straight-leg jeans, black combat boots, and black crossbody…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: Scored this bootleg 2003 tour graphic tee on depop for $24 and I'm obsessed. Threw it on with some baggy denim…
  try 1: completed — fit card 217 chars


impossible query stops early  (example wardrobe)
  query: designer ballgown size XXS under $5
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit
  try 1: stopped early — Nothing in the listings matched description 'designer ballgo
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit
 
empty wardrobe  (empty wardrobe)
  query: denim jacket under $50
[1] parse_query
      in:  denim jacket under $50
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
      out: 5 items: Denim Jacket — Light Wash, Cropped, 90s Track Jacket — Navy/White Stripe, High-Waisted Denim Shorts — Cutoff … +2 more
      →    5 match(es)
[3] select_item
      out: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
[4] suggest_outfit
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: Outfit 1: Throw that cropped Wrangler jacket over a simple white crewneck tee, high-waisted black straight-leg…
      →    0 wardrobe item(s)
[5] create_fit_card
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: Scored this cropped Wrangler denim jacket on Poshmark for $42 and it has the absolute best vintage streetwear …
  try 1: completed — fit card 320 chars
[1] parse_query
      in:  denim jacket under $50
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
      out: 5 items: Denim Jacket — Light Wash, Cropped, 90s Track Jacket — Navy/White Stripe, High-Waisted Denim Shorts — Cutoff … +2 more
      →    5 match(es)
[3] select_item
      out: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
[4] suggest_outfit
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: Outfit 1: Throw that cropped Wrangler jacket over a simple white crewneck tee, high-waisted black straight-leg…
      →    0 wardrobe item(s)
[5] create_fit_card
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: Found this cropped Wrangler denim jacket on Poshmark for forty-two dollars and honestly haven't taken it off s…
 
session consistency  (example wardrobe)
  query: 90s track jacket in size M
[1] parse_query
      in:  90s track jacket in size M
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': '90s track jacket in', 'size': 'M', 'max_price': None}
      out: 4 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +1 more
      →    4 match(es)
[3] select_item
      out: 90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
[4] suggest_outfit
      in:  90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      out: Outfit 1: Pair the 90s Track Jacket — Navy/White Stripe with your white ribbed tank top, baggy straight-leg je…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  90s Track Jacket — Navy/White Stripe ($45.0, poshmark)
      out: Scored this vintage Champion track jacket on Poshmark for just $45 and I'm obsessed. It's giving major 90s str…
  try 1: completed — fit card 218 chars


fit card with descriptions  (example wardrobe)
  query: platform sneakers size 8
[1] parse_query
      in:  platform sneakers size 8
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'platform sneakers size 8', 'size': None, 'max_price': None}
      out: 5 items: Platform Sneakers — White Chunky Sole, Platform Mary Janes — Black Patent, Low-Top Canvas Sneakers — Off-White … +2 more
      →    5 match(es)
[3] select_item
      out: Platform Sneakers — White Chunky Sole ($48.0, poshmark)
  [rate limit] 15 requests used this minute. Waiting 39s. This is normal.
[4] suggest_outfit
      in:  Platform Sneakers — White Chunky Sole ($48.0, poshmark)
      out: **Outfit 1: The Off-Duty Streetwear Look** Pair your new Platform Sneakers with the white ribbed tank top, bag…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Platform Sneakers — White Chunky Sole ($48.0, poshmark)
      out: Found these chunky platform sneakers on Poshmark for $48 and I am officially in my 90s streetwear era. They ad…
  try 1: completed — fit card 256 chars


max price test  (example wardrobe)
  query: silk slip dress in midi length under $40
[1] parse_query
      in:  silk slip dress in midi length under $40
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'silk slip dress in midi length', 'size': None, 'max_price': 40.0}
      out: 5 items: 90s Silk Slip Dress — Floral, Midi Length, Y2K Baby Tee — Butterfly Print, High-Waisted Denim Shorts — Cutoff … +2 more
      →    5 match(es)
[3] select_item
      out: 90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
  [rate limit] 15 requests used this minute. Waiting 3s. This is normal.
[4] suggest_outfit
      in:  90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
      out: Outfit 1: Layer the 90s Silk Slip Dress over your white ribbed tank top and ground the feminine floral pattern…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
      out: Scored this 90s silk slip dress on Depop for just $30 and I am so obsessed with the floral print. It's giving …
  try 1: completed — fit card 288 chars

Wrote results\run_2026-11-26_2033_before.md
50 model calls this session, 15571 prompt + 5378 output tokens

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

     In criterion 4, one of the tries failed and did not mention that the sneakers were white. 

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Full three-tool run returns a fit card | 4 of 5 | MET | checked each try and saw that at least 4 of them had a fit card |
| 2 | Empty search stops before tool 2 | 5 of 5 | MET | checked each try with an input not in the listings. The trace showed that none of the tries went past tool 2 |
| 3 | Item in session matches item passed on | 5 of 5 | MET | using the trace, it was possible to see that the session item stayed the same for each of the tries |
| 4 | Fit card mentions the item's description | 3 of 5 | MET | read through the fitcard and decipher if it included key words from the item description |
| 5 | Over-budget query returns nothing over the limit | 4 of 5 | MET | checked the price of the item returned |



**Diagnoses**

I have met all of my criteria. The only criteria that failed in one of the 5 tries was criteria 4. The item description was "White chunky platform sneakers. Very late 90s / early 2000s energy. Velcro straps. True to size. Some sole yellowing." In testing I decided to focus on making sure the key words white, chunky platform sneakes, 90s, were in the description. One of the fit cards failed to mention that the sneakers were white.

This issue could be caused by an improper prompt. I should specify in the prompt to use the item description in the fitcard.


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] parse_query
      in:  red shoes under $200
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'red shoes', 'size': None, 'max_price': 200.0}
      out: 1 items: Oversized College Crewneck — Faded Red
      →    1 match(es)
[3] select_item
      out: Oversized College Crewneck — Faded Red ($21.0, thredUp)
[4] suggest_outfit
      in:  Oversized College Crewneck — Faded Red ($21.0, thredUp)
      out: Outfit 1: The Classic Streetwear Vibe Pair the Oversized College Crewneck — Faded Red with your Baggy straight…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Oversized College Crewneck — Faded Red ($21.0, thredUp)
      out: Score this faded red college crewneck on thredUp for just $21 and I am never taking it off. Threw it on with d…

  Found:    Oversized College Crewneck — Faded Red — $21.0 on thredUp

  Outfit:   Outfit 1: The Classic Streetwear Vibe
Pair the Oversized College Crewneck — Faded Red with your Baggy straight-leg jeans, dark wash, and finish it with your Chunky white sneakers and Black crossbody bag. Let the white ribbed tank top peekout just a bit at the neckline. 
Why it works: The faded red pops against the deep indigo denim, and the chunky sneakers balance out the relaxed, oversized silhouette of the sweater for an effortless, sporty look.

Outfit 2: The Casual Contrast Look
Wear the Oversized College Crewneck — Faded Red tucked into your Wide-leg khaki trousers, accented with the Brown leather belt, and step into your Black combat boots. Throw on the Vintage black denim jacket over top if you need an extra layer.
Why it works: Pairing the athletic red crewneck with crisp khaki trousers creates a cool high-low mix, while the brown belt and black boots add grounding earth tones and a touch of edge.

  Fit card: Score this faded red college crewneck on thredUp for just $21 and I am never taking it off. Threw it on with dark wash straight jeans and chunky sneakers for an effortless streetwear vibe.It has that perfectly worn-in look that makes it feel like an actual vintage thrift find.

2 model calls this session, 717 prompt + 262 output tokens
```

**Empty search**

```
[1] parse_query
      in:  designer ball gown under $60 size XXS
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  {'description': 'designer ball gown', 'size': 'XXS', 'max_price': 60.0}
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit

  Nothing in the listings matched description 'designer ball gown', size XXS, under $60.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $60.

0 model calls this session
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
