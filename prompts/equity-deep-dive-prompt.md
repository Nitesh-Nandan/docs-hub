# Equity Deep-Dive Prompt (document-driven)

A reusable prompt for tearing apart a single listed company when **you supply the
source documents** (annual report, concalls, chart, Screener snapshot, shareholding).

Different from [fundamental-research.md](../fundamental-research.md), which is the
API/web-driven 7-lens framework. Use this one when you have the PDFs in hand and
want an adversarial read of them.

---

## Step 1 — Gather the documents

Attach as many as you can. The prompt tells the analyst to flag what's missing
rather than fill gaps with guesses.

| # | Document | Where to get it | Priority |
|---|---|---|---|
| 1 | Annual Report — last 2–3 years | BSE/NSE filings or company website (Investors page) | Must |
| 2 | MD&A (Management Discussion & Analysis) | Inside the same annual report PDF | Must |
| 3 | Concall transcripts — last 2–3 quarters | Screener.in (Documents tab) or Tijori Finance | Must |
| 4 | Screener.in snapshot | screener.in/company/`SYMBOL` — P/E, ROE, D/E, revenue & profit growth, operating cash flow, promoter holding | Must |
| 5 | Shareholding pattern — latest quarter | BSE/NSE filings, or Screener's shareholding tab | Must |
| 6 | Daily (1D) chart screenshot | TradingView with 50 EMA, 200 EMA, RSI(14), Volume | Nice to have |
| 7 | Quarterly results / investor presentation — latest | Company website or Screener | Nice to have |

Tip: 3 years of annual reports beats 1. Tone drift between years is where the
management-DNA lens gets its signal.

---

## Step 2 — The prompt

Copy everything below, replace `[COMPANY NAME]`, attach the documents.

---

> Act as a seasoned equity research analyst with 20 years of experience across
> fundamental analysis, technical analysis, and behavioral finance.
>
> I am providing you documents for **[COMPANY NAME]**: annual reports, MD&A,
> concall transcripts, a daily technical chart, key ratios from Screener, and the
> latest shareholding pattern.
>
> Tear this company apart across the six dimensions below. Cite the specific
> document, page, or quote behind every claim. If a document I've given you does
> not support a conclusion, say so — do not fill the gap with generic industry
> knowledge or assumptions. If a needed document is missing, name it and state
> what you could not assess without it.
>
> **1. FUNDAMENTALS — is the business genuinely healthy, or does it just look good on the surface?**
> - Revenue quality: organic vs acquired, recurring vs one-off, customer/geography concentration
> - Margin trajectory over 3 years — and *why* it moved, not just that it moved
> - Cash flow vs reported profit: OCF/EBITDA conversion, receivable days, inventory days
> - Debt structure: gross vs net, maturity profile, interest coverage, off-balance-sheet items
> - ROE sustainability: decompose it — is it margin, asset turns, or leverage doing the work?
> - Accounting red flags: related-party transactions, capitalised expenses, auditor
>   change or qualified opinion, contingent liabilities, unusual "other income"
>
> **2. MANAGEMENT DNA — read between the lines of the concalls and MD&A.**
> - Confident or defensive? How do they handle hostile analyst questions —
>   answer directly, deflect, or filibuster?
> - Track record: pull their guidance from 4–8 quarters ago and check it against
>   what was actually delivered. Overpromise-underdeliver is a pattern, not an event.
> - Language-tone drift vs last year — which words appeared, which quietly vanished?
> - Capital allocation history: where did the cash go, and did it earn a return?
> - **Promoter pledge or stake reduction is an automatic red flag — call it out explicitly,
>   with the quarter-on-quarter numbers.**
> - Also check: FII/DII direction, and whether any marquee institution exited.
>
> **3. VALUATION REALITY — is the market pricing in perfection?**
> - Current P/E and EV/EBITDA vs the company's own 3Y and 5Y medians
> - Same multiples vs 3–4 named sector peers, and say who is cheap for a *reason*
> - PEG against realistic (not management-guided) earnings growth
> - What growth rate is the current price implying? Is that rate credible given
>   dimension 1 and 2?
> - Tell me plainly if I am paying a premium for growth that may never arrive.
>
> **4. TECHNICAL STRUCTURE — where is the stock in its trend cycle?**
> - Wyckoff phase: accumulation, markup, distribution, or markdown — and the evidence
> - Price vs 50 EMA and 200 EMA; is the 200 EMA rising, flat, or rolling over?
> - Key support and resistance levels with actual price numbers
> - Is volume confirming price, or diverging? Call out distribution days on rallies.
> - RSI: overbought/oversold, and any divergence vs price
>
> **5. RISK FACTORS — the three things that could destroy this thesis.**
> Give exactly three, each with (a) the mechanism of damage, (b) rough likelihood,
> (c) what early warning sign I should monitor. Cover company-specific, sector, and
> macro risk — one of each if the facts support it.
>
> **6. FINAL VERDICT**
> - **BUY / HOLD / AVOID** — pick one, no hedging
> - **Conviction score out of 10** with a one-line justification of the number
> - **Price at which this becomes interesting**, if not now — a number, plus the
>   condition that would have to be true at that price
> - **The bear case in one sentence** — the strongest argument against my buying this
> - **One line that summarizes this stock**
>
> Do not give me a balanced, diplomatic answer. Lead with what is wrong before what
> is right. I want the truth even if it is uncomfortable — but every uncomfortable
> claim must be traceable to something in the documents.

---

## Step 3 — Sanity-check the answer

Before acting on the output, run these checks. A confident-sounding report that
fails any of them is not usable.

- **Every number is sourced.** If a figure can't be pointed back to a document,
  treat it as invented.
- **The verdict follows the evidence.** A BUY on top of two unresolved accounting
  red flags is a contradiction — push back and ask it to reconcile.
- **The bear case is real.** If the one-sentence bear case is weak or generic, the
  analysis didn't try hard enough. Ask again: "give me the strongest bear case, as
  a short-seller would write it."
- **Cross-check the technicals** against the `lab` DB (`historical_day_candles`) —
  chart screenshots are easy to misread.
- **Reconcile with the 7-lens verdict** in [fundamental-research.md](../fundamental-research.md)
  if you've run that too. Two frameworks disagreeing is information.

---

## Conviction score rubric

For consistency across companies, anchor the /10 like this:

| Score | Meaning |
|---|---|
| 9–10 | Rare. Exceptional business, clear tailwind, price still reasonable. Size up. |
| 7–8 | Strong business, fair-to-slightly-rich price. Buy, normal position size. |
| 5–6 | Good company, wrong price or unclear timing. WATCH with a price alert. |
| 3–4 | Real flaws in business quality, governance, or valuation. Pass. |
| 1–2 | Avoid entirely — pledge, accounting, or structural decline. |

Most companies land at 4–6. If everything scores 8, the scale is broken.
