#!/usr/bin/env python3
"""2026 US Tariff, CBP MPF, Landed-Cost & Multi-Channel (TikTok Shop / Etsy / Shopify) Repricing CLI.

Interactive browser version (no login):
  - US Tariff Calculator: https://rerivo.com/tools/tariff-landed-cost-calculator/
  - TikTok Shop & Etsy Fee Calculator: https://rerivo.com/tools/tiktok-shop-fee-calculator/
"""
import argparse
import json
import math


def ceil_cents(value: float) -> float:
    return max(0.0, math.ceil(value * 100.0 - 1e-9) / 100.0)


def calculate_tariff_reprice(
    qty: int = 500,
    fob: float = 6.80,
    freight_total: float = 920.0,
    mfn_rate: float = 6.5,
    sec301_rate: float = 25.0,
    extra_duty_rate: float = 20.0,
    entry_type: str = "formal",
    brokerage: float = 145.0,
    platform_fee_rate: float = 15.0,
    current_price: float = 29.0,
    target_margin_rate: float = 48.0,
) -> dict:
    customs_value = round(qty * fob, 2)
    stacked_rate = mfn_rate + sec301_rate + extra_duty_rate
    duty_total = round(customs_value * (stacked_rate / 100.0), 2)
    mpf_total = (
        round(min(614.35, max(31.67, customs_value * 0.003464)), 2)
        if entry_type == "formal"
        else 2.77
    )
    pre_tariff_per_unit = round((customs_value * (1.0 + mfn_rate / 100.0) + freight_total) / qty, 2)
    landed_per_unit = round((customs_value + duty_total + mpf_total + brokerage + freight_total) / qty, 2)
    unit_cost_jump = round(landed_per_unit - pre_tariff_per_unit, 2)

    fee = platform_fee_rate / 100.0
    target_m = target_margin_rate / 100.0
    prior_profit = round(current_price * (1.0 - fee) - pre_tariff_per_unit, 2)
    current_profit = round(current_price * (1.0 - fee) - landed_per_unit, 2)
    current_margin_pct = round((current_profit / current_price) * 100.0, 1)

    profit_preserving_price = ceil_cents((prior_profit + landed_per_unit) / (1.0 - fee))
    target_reprice = ceil_cents(landed_per_unit / (1.0 - fee - target_m))
    naive_pass_through = round(current_price + unit_cost_jump, 2)
    batch_fee_drag_saved = round(max(0.0, (target_reprice - naive_pass_through) * qty), 2)

    return {
        "customs_value": customs_value,
        "stacked_duty_rate_pct": stacked_rate,
        "duty_total": duty_total,
        "mpf_total": mpf_total,
        "pre_tariff_per_unit": pre_tariff_per_unit,
        "landed_per_unit": landed_per_unit,
        "unit_cost_jump": unit_cost_jump,
        "current_profit_per_unit": current_profit,
        "current_margin_pct": current_margin_pct,
        "profit_preserving_price": profit_preserving_price,
        "target_margin_reprice": target_reprice,
        "batch_fee_drag_saved": batch_fee_drag_saved,
    }


def calculate_multichannel_payout(
    cogs: float = 7.20,
    pack_ship: float = 6.00,
    list_price: float = 38.00,
    promo_rate: float = 10.0,
    tiktok_ref_rate: float = 6.0,
    tiktok_affiliate_rate: float = 15.0,
    sample_subsidy: float = 1.50,
    etsy_total_rate: float = 24.5,
    target_margin_rate: float = 35.0,
) -> dict:
    net_sale = round(list_price * (1.0 - promo_rate / 100.0), 2)
    unit_cost = cogs + pack_ship
    shopify_net = round(net_sale * (1.0 - 0.029) - 0.30 - unit_cost, 2)
    etsy_net = round(net_sale * (1.0 - etsy_total_rate / 100.0) - 0.25 - unit_cost, 2)
    tiktok_net = round(
        net_sale * (1.0 - (tiktok_ref_rate + tiktok_affiliate_rate) / 100.0) - sample_subsidy - unit_cost,
        2,
    )
    payout_spread = round(shopify_net - tiktok_net, 2)

    ref = tiktok_ref_rate / 100.0
    aff = tiktok_affiliate_rate / 100.0
    tm = target_margin_rate / 100.0
    promo = promo_rate / 100.0

    max_affil_pct = round(
        max(0.0, ((net_sale * (1.0 - ref - tm) - unit_cost - sample_subsidy) / net_sale) * 100.0),
        2,
    )
    tiktok_target_list = ceil_cents((unit_cost + sample_subsidy) / ((1.0 - ref - aff - tm) * (1.0 - promo)))

    return {
        "realized_sale": net_sale,
        "shopify_net": shopify_net,
        "etsy_net": etsy_net,
        "tiktok_net": tiktok_net,
        "payout_spread": payout_spread,
        "max_affiliate_pct": max_affil_pct,
        "tiktok_target_list": tiktok_target_list,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="US Tariff Landed-Cost & Multi-Channel Fee Repricing CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("tariff", help="Calculate stacked US tariff, CBP MPF & target-margin reprice")
    t.add_argument("--qty", type=int, default=500)
    t.add_argument("--fob", type=float, default=6.80)
    t.add_argument("--freight", type=float, default=920.0)
    t.add_argument("--mfn", type=float, default=6.5)
    t.add_argument("--sec301", type=float, default=25.0)
    t.add_argument("--extra", type=float, default=20.0)
    t.add_argument("--entry", choices=["formal", "informal"], default="formal")
    t.add_argument("--brokerage", type=float, default=145.0)
    t.add_argument("--fee", type=float, default=15.0)
    t.add_argument("--price", type=float, default=29.0)
    t.add_argument("--margin", type=float, default=48.0)

    m = sub.add_parser("multichannel", help="Compare Shopify vs Etsy Offsite Ads vs TikTok Shop payouts")
    m.add_argument("--cogs", type=float, default=7.20)
    m.add_argument("--pack-ship", type=float, default=6.00)
    m.add_argument("--price", type=float, default=38.00)
    m.add_argument("--promo", type=float, default=10.0)
    m.add_argument("--ref", type=float, default=6.0)
    m.add_argument("--affiliate", type=float, default=15.0)
    m.add_argument("--sample", type=float, default=1.50)
    m.add_argument("--etsy-rate", type=float, default=24.5)
    m.add_argument("--margin", type=float, default=35.0)

    args = parser.parse_args()
    if args.cmd == "tariff":
        res = calculate_tariff_reprice(
            qty=args.qty,
            fob=args.fob,
            freight_total=args.freight,
            mfn_rate=args.mfn,
            sec301_rate=args.sec301,
            extra_duty_rate=args.extra,
            entry_type=args.entry,
            brokerage=args.brokerage,
            platform_fee_rate=args.fee,
            current_price=args.price,
            target_margin_rate=args.margin,
        )
    else:
        res = calculate_multichannel_payout(
            cogs=args.cogs,
            pack_ship=args.pack_ship,
            list_price=args.price,
            promo_rate=args.promo,
            tiktok_ref_rate=args.ref,
            tiktok_affiliate_rate=args.affiliate,
            sample_subsidy=args.sample,
            etsy_total_rate=args.etsy_rate,
            target_margin_rate=args.margin,
        )
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
