"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

_STOPWORDS = {"a", "an","and", "the", "for", "with", "under", "over", "in", "of"
             }

def _keywords(text:str) -> set[str]:
    """Lowercase words worth matching on, stopwards removed."""
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 1}


def _size_tokens(size: str) -> set[str]:
    cleaned = re.sub(r"\([^)]*\)", " ", size or "") # drop parentheticals
    parts = [p.strip().upper() for p in cleaned.split("/")]
    
    return {p for p in parts if p}

def _size_matches(wanted: str, listing_size: str) -> bool:
    if not wanted:
        return True
    listing_tokens = _size_tokens(listing_size)   
    if any(token.startswith("ONE SIZE") for token in listing_tokens):
        return True
    return bool(_size_tokens(wanted) & listing_tokens)
    

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    # TODO: replace this with your implementation
    
    #Step 1 - create listing from load listing
    listings = load_listings()

    # Step 2 - Filter by price
    if max_price:
    # create listings and filter by price
        listings = [item for item in listings if item["price"] <= max_price]
    #print("Listings filtered by price")
    
    # Step 2 Filter by size
    if size:
        listings = [item for item in listings if _size_matches(size, item["size"])]

    # Step 3 - score with keyword overlap and description
    matches = {}
    for item in listings:
        # print(f"description {_keywords(description)}")
        # print(f"listing {_keywords(item['description'])}")

        for i in _keywords(description):
            for j in _keywords(item["description"]):
                # so the issue with this solution is that i can't use a dictionary as a key. so i'll just use the id for the dictionary as one.
                if i == j:
                    if item["id"] not in matches:
                        matches[item["id"]] = 1
                    else:
                        matches[item["id"]] += 1
    # Step 4 - Drop anything scoring 0. If none of the keywords match, they won't get added to the mathes dictionary
    # Step 5 sorting by score
    sorted_desc = dict(sorted(matches.items(), key=lambda item: item[1], reverse=True))
    #print(sorted_desc)

    result = []

    # attempt at sorting before
    # for l in listings:
    #     if len(result) == config.SEARCH_RESULT_LIMIT:
    #         break
    #     for k,v in sorted_desc.items():
    #         #result.append(l[k])
    #         if l["id"] == k:
    #             result.append(l)
    #         if len(result) == config.SEARCH_RESULT_LIMIT:
    #             break

    # attempt at sorting after
    for k,v in sorted_desc.items():
        if len(result) == config.SEARCH_RESULT_LIMIT:
            break
        for l in listings:
            if l["id"] == k:
                result.append(l)
            if len(result) == config.SEARCH_RESULT_LIMIT:
                break

         
    #print("the output")
    return result



# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    system = (
        "You are a friendly thrift-store stylist. Give concrete, wearable outfit "
        "ideas in plain text. Keep it short: one or two outfits, a few lines each."
    )

    # Describe the new item. brand is often None, so only mention it if present.
    item_desc = (
        f"{new_item.get('title', 'Unnamed item')} "
        f"({new_item.get('category', 'unknown category')}, "
        f"colors: {', '.join(new_item.get('colors') or []) or 'unknown'}, "
        f"style: {', '.join(new_item.get('style_tags') or []) or 'unknown'})"
    )
    if new_item.get("brand"):
        item_desc += f", brand: {new_item['brand']}"

    # Step 1 - check whether the wardrobe is empty
    items = (wardrobe or {}).get("items") or []

    if not items:
        # Step 2 - no wardrobe, so ask for general styling ideas
        prompt = (
            f"I'm thinking about buying this thrifted item: {item_desc}.\n"
            "I haven't shared my wardrobe, so suggest one or two outfits built "
            "around it using common basics (e.g. jeans, white tee, sneakers), "
            "plus a quick styling tip."
        )
    else:
        # Step 3 - format the wardrobe into the prompt and ask for specific combos
        wardrobe_lines = []
        for w in items:
            line = (
                f"- {w.get('name', 'unnamed')} ({w.get('category', '?')}; "
                f"colors: {', '.join(w.get('colors') or []) or '?'}; "
                f"style: {', '.join(w.get('style_tags') or []) or '?'})"
            )
            if w.get("notes"):
                line += f" — notes: {w['notes']}"
            wardrobe_lines.append(line)

        prompt = (
            f"I'm thinking about buying this thrifted item: {item_desc}.\n\n"
            "Here's what's already in my wardrobe:\n"
            + "\n".join(wardrobe_lines)
            + "\n\nSuggest one or two outfits that pair the new item with "
            "specific pieces I already own. Name each wardrobe piece exactly as "
            "listed, and say briefly why the combination works."
        )

    # Step 4 - return the model's response, never an empty string
    response = generate(prompt, system=system)
    if not response or not response.strip():
        return (
            f"Try pairing the {new_item.get('title', 'item')} with simple "
            "neutral basics and let it be the statement piece."
        )
    return response.strip()


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # Step 1 - guard against an empty or whitespace-only outfit
    if not outfit or not outfit.strip():
        return (
            "Couldn't write a fit card: no outfit suggestion was provided. "
            "Run suggest_outfit() first and pass its result in."
        )

    system = (
        "You write short, casual social media captions about thrift finds. "
        "Sound like a real person posting their fit, not a product listing. "
        "Two to four sentences. Plain text, no hashtag walls."
    )

    # Step 2 - build a prompt with the item details and the outfit
    title = new_item.get("title", "this piece")
    price = new_item.get("price")
    price_text = f"${price:.2f}" if isinstance(price, (int, float)) else "a steal"
    platform = new_item.get("platform") or "a thrift shop"

    item_desc = (
        f"Item: {title}\n"
        f"Price: {price_text}\n"
        f"Platform: {platform}\n"
        f"Colors: {', '.join(new_item.get('colors') or []) or 'unknown'}\n"
        f"Style: {', '.join(new_item.get('style_tags') or []) or 'unknown'}"
    )
    # brand is None for most listings, so only include it when present
    if new_item.get("brand"):
        item_desc += f"\nBrand: {new_item['brand']}"

    prompt = (
        f"{item_desc}\n\n"
        f"How I'm styling it:\n{outfit.strip()}\n\n"
        "Write a caption for posting this fit. Mention the item, the price, and "
        "the platform exactly once each, and be specific about the vibe. Mention the item description: {new_item['description']}"
    )

    # Step 3 - call the model and return its response, never an empty string
    response = generate(prompt, system=system)
    if not response or not response.strip():
        return f"Thrifted this {title} for {price_text} on {platform} and I'm obsessed."
    return response.strip()
