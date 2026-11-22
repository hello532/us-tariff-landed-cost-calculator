# 2026 US Tariff, CBP MPF, Landed-Cost & Multi-Channel Fee Repricing Calculator

Open-source Python CLI and Excel formula reference for e-commerce importers, Amazon FBA sellers, Shopify brands, TikTok Shop operators, and Etsy sellers modeling **post-*de minimis* US tariffs**, **formal/informal CBP Merchandise Processing Fees (MPF)**, **marketplace fee-on-tariff drag**, and **TikTok Shop creator affiliate commission caps**.

> **Prefer a zero-login browser calculator or ready-to-use Excel workbook?**
> - **Free US Tariff & Landed Cost Browser Calculator** (instant CSV + shareable URL): https://rerivo.com/tools/tariff-landed-cost-calculator/
> - **Free TikTok Shop, Etsy & Shopify Fee Browser Calculator**: https://rerivo.com/tools/tiktok-shop-fee-calculator/
> - **Free 5-SKU Excel Starters (`.xlsx`, zero signup)**: [tariff-landed-cost-lite.xlsx](https://rerivo.com/free/tariff-landed-cost-lite.xlsx) · [multi-channel-seller-fee-lite.xlsx](https://rerivo.com/free/multi-channel-seller-fee-lite.xlsx)

---

## Why Naive Pass-Through Pricing Leaks Margin

1. **Stacked US Tariffs + Formal CBP MPF**: Base MFN, Section 301, and reciprocal tariffs stack additively on Customs FOB value, plus Formal Entry MPF (`0.3464%`, clamped between **$31.67** and **$614.35**).
2. **Marketplace Fee-on-Tariff Drag**: If duty + brokerage adds `+$3.41/unit` to your landed cost and you raise retail by only `+$3.41`, Amazon/Etsy/TikTok still takes ~15% referral fee on that extra `$3.41` (`-$0.51/unit` silently lost).
3. **TikTok Shop Multi-Layer Deductions**: A 10% seller coupon + 6% referral + 15% creator affiliate + `$1.50` amortized free sample cost drops a `$38` SKU's net payout from **$19.71 on Shopify** to **$12.32 on TikTok Shop** (`-$7.39/order`).

---

## Copy-Paste Excel Formulas

### 1. US Tariff, CBP MPF & Target-Margin Repricing

| Metric (Row 2) | Exact Excel Formula | Worked 500-Unit Example (`$6.80` FOB, 51.5% duty) |
| --- | --- | --- |
| Batch Customs FOB (`C2`) | `=A2*B2` | `$3,400.00` |
| Stacked US Duty (`D2`) | `=C2*(E2+F2+G2)` | `$1,751.00` (`51.5%`) |
| Formal CBP MPF Clamped (`H2`) | `=MIN(614.35, MAX(31.67, C2*0.003464))` | `$31.67` |
| Loaded Landed Unit Cost (`I2`) | `=(C2+D2+H2+Brokerage+Freight)/A2` | `$12.50 / unit` |
| Dollar-Profit Preserving Price (`J2`) | `=CEILING((PriorProfit+I2)/(1-FeePct), 0.01)` | `$33.03` |
| Target-Margin Retail Reprice (`K2`) | `=CEILING(I2/(1-FeePct-TargetMarginPct), 0.01)` | `$33.79` (`48%` margin) |

### 2. TikTok Shop, Etsy Offsite Ads & Shopify Payout Parity

| Metric (Row 2) | Exact Excel Formula | Worked `$38` SKU Example (`10%` coupon) |
| --- | --- | --- |
| Realized Sale After Coupon (`C2`) | `=ListPrice*(1-CouponPct)` | `$34.20` |
| Shopify Direct Net Payout (`D2`) | `=C2*(1-0.029)-0.30-COGS-ShipLabel` | `$19.71` (`57.6%`) |
| TikTok Shop Net Payout (`E2`) | `=C2*(1-RefPct-AffilPct)-SampleDrag-COGS-ShipLabel` | `$12.32` (`36.0%`) |
| Max Affordable Creator Affiliate % (`F2`) | `=MAX(0, (C2*(1-RefPct-TargetMargin)-COGS-ShipLabel-SampleDrag)/C2)` | **`16.02%` cap** |
| TikTok Target List Reprice (`G2`, `35%` floor) | `=CEILING((COGS+ShipLabel+SampleDrag)/((1-RefPct-AffilPct-TargetMargin)*(1-CouponPct)), 0.01)` | `$37.13` |

---

## Quick CLI Usage (Python 3, Zero Dependencies)

```bash
# 1. Run default 500-unit US Tariff + CBP MPF scenario
python3 tariff_calc.py tariff

# 2. Custom SKU tariff scenario
python3 tariff_calc.py tariff --qty 1000 --fob 5.20 --freight 1400 --mfn 4.0 --sec301 25.0 --extra 20.0 --fee 15 --price 24.99 --margin 45

# 3. Compare TikTok Shop vs Etsy Offsite Ads vs Shopify payouts
python3 tariff_calc.py multichannel --cogs 7.20 --pack-ship 6.00 --price 38 --promo 10 --affiliate 15 --sample 1.50
```

Run unit tests:

```bash
python3 -m unittest test_tariff_calc.py -v
```

---

## Need Multi-SKU Excel Workbooks (250 SKUs, Zero Subscription)?

If you don't want to wire 250 SKUs, CBM container freight splits, and channel sensitivity matrices by hand:

- **250-SKU US Tariff, De Minimis & Landed-Cost Excel Repricer ($24 one-time)** — unlocked `.xlsx` + offline HTML Decision Desk: https://rerivo.com/products/tariff-landed-cost-repricer/
- **250-SKU Multi-Channel Seller Fee & TikTok Shop Repricer ($19 one-time)** — unlocked `.xlsx` + offline HTML Decision Desk: https://rerivo.com/products/multi-channel-seller-fee-repricer/
- **Worked Method Guides**: [How to Calculate US Tariff Landed Cost](https://rerivo.com/guides/calculate-tariff-landed-cost/) · [How to Price SKUs Across TikTok Shop, Etsy & Shopify](https://rerivo.com/guides/calculate-tiktok-shop-multi-channel-fees/)

## License

MIT — see [LICENSE](LICENSE).
