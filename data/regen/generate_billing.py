"""
Accord - billing data generator / re-age routine.

Rebuilds Billing Statements, Payments, Promises to Pay and Adjustments for the
88 Residential Agreement accounts, anchored to AS_OF, so the delinquency
distribution matches docs/data-plan.md on the day it is loaded:
  Current 52 | 1-30 DPD 14 | 31-60 DPD 10 | 61-90 DPD 7 | 90+ DPD 5
Rerun with a new AS_OF before UAT or a demo to re-age the book.
Seeded defects preserved: 3 status mismatches (ACC-0001..0003), 5 promises with
no related statement.
"""
import csv, random, os, sys
from datetime import date, timedelta

AS_OF = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
OUT = sys.argv[2] if len(sys.argv) > 2 else "."
rng = random.Random(20261008)

PAY = {1:164.28,2:194.61,3:209.23,4:167.34,5:181.26,6:140.24,7:159.72,8:120.27,9:207.92,10:135.39,
11:201.23,12:213.92,13:121.38,14:126.65,15:161.14,16:157.91,17:187.36,18:157.54,19:144.34,20:208.02,
21:189.96,22:200.41,23:214.62,24:190.63,25:126.84,26:208.16,27:135.45,28:167.92,29:164.56,30:221.60,
31:222.09,32:130.81,33:189.04,34:197.44,35:181.77,36:148.66,37:185.20,38:127.31,39:129.02,40:124.32,
41:192.62,42:163.68,43:173.56,44:193.43,45:143.59,46:214.29,47:197.68,48:184.28,49:199.68,50:166.42,
51:178.18,52:201.16,53:134.69,54:161.40,55:122.50,56:216.63,57:175.31,58:187.73,59:177.48,60:199.99,
61:210.23,62:121.98,63:177.92,64:212.08,65:186.14,66:209.27,67:171.31,68:219.13,69:164.90,70:152.79,
71:170.63,72:157.65,73:188.40,74:149.04,75:134.67,76:162.05,77:212.76,78:129.36,79:139.08,80:174.67,
81:183.74,82:147.48,83:129.33,84:180.78,85:220.91,86:136.87,87:152.10,88:205.79}

BUCKETS = {
 "90+":   ([22,30,40,53,59], (95,150)),
 "61-90": ([9,21,26,51,67,83,84], (63,88)),
 "31-60": ([1,2,3,6,11,43,58,73,87,28], (33,58)),
 "1-30":  ([8,23,39,46,52,64,65,82,12,24,35,47,61,80], (3,28)),
}
MISMATCH = {1,2,3}            # past due but left marked Current (Phase 7 fixes)
BROKEN_CLUSTER = [26,51,84,30]  # repeat promise breakers

def acc(n): return f"ACC-{n:04d}"
def svc(n): return f"SVC-{n:04d}"
def add_months(d, m):
    y, mo = d.year + (d.month - 1 + m) // 12, (d.month - 1 + m) % 12 + 1
    day = min(d.day, 28)
    return date(y, mo, day)

bucket_of = {a:(b,r) for b,(lst,r) in BUCKETS.items() for a in lst}
stmts, pays, accounts, svcs = [], [], [], []
by_acc = {}
sid = pid = 0

def new_stmt(a, due, amount):
    global sid
    sid += 1
    s = dict(Legacy_Id__c=f"STM-{sid:05d}", acc=a, Statement_Date__c=due - timedelta(days=21),
             Due_Date__c=due, Amount_Due__c=amount, paid=0.0, Status__c=None)
    stmts.append(s); by_acc.setdefault(a, []).append(s); return s

def new_pay(s, amount, when):
    global pid
    pid += 1
    when = min(when, AS_OF)
    when = max(when, s["Statement_Date__c"])
    pays.append({"Billing_Statement__r.Legacy_Id__c": s["Legacy_Id__c"], "Amount__c": f"{amount:.2f}",
                 "Payment_Date__c": when.isoformat(),
                 "Method__c": rng.choices(["ACH","Card","Check"], [60,32,8])[0],
                 "External_Reference__c": f"PMT-{pid:05d}"})
    s["paid"] = round(s["paid"] + amount, 2)

dpd_target = {}
for a in range(1, 89):
    amt = PAY[a]
    if a in bucket_of:
        b, (lo, hi) = bucket_of[a]
        d = rng.randint(lo, hi); dpd_target[a] = d
        oldest_unpaid = AS_OF - timedelta(days=d)
        # unpaid run: oldest_unpaid, +1 month ... up to AS_OF+20
        unpaid = [oldest_unpaid]
        while add_months(unpaid[-1], 1) <= AS_OF + timedelta(days=20):
            unpaid.append(add_months(unpaid[-1], 1))
        p = rng.randint(2, 7)
        paid_dues = [add_months(oldest_unpaid, -k) for k in range(p, 0, -1)]
        for due in paid_dues:
            s = new_stmt(a, due, amt); new_pay(s, amt, due - timedelta(days=rng.randint(0, 10)))
        for i, due in enumerate(unpaid):
            s = new_stmt(a, due, amt)
            if rng.random() < 0.3 and due <= AS_OF:   # partial payment
                new_pay(s, round(amt * rng.uniform(0.25, 0.6), 2), due + timedelta(days=rng.randint(1, 15)))
    else:
        n = rng.randint(3, 12)
        last = AS_OF + timedelta(days=rng.randint(-25, 20))
        dues = [add_months(last, -k) for k in range(n - 1, -1, -1)]
        for due in dues:
            s = new_stmt(a, due, amt)
            if due <= AS_OF:
                new_pay(s, amt, due - timedelta(days=rng.randint(0, 10)))
            elif rng.random() < 0.3:
                new_pay(s, amt, s["Statement_Date__c"] + timedelta(days=rng.randint(1, 10)))
    first_due = by_acc[a][0]["Due_Date__c"]
    svcs.append({"Legacy_Id__c": svc(a), "Activation_Date__c": (first_due - timedelta(days=30)).isoformat(),
                 "First_Due_Date__c": first_due.isoformat()})

for s in stmts:
    bal = round(s["Amount_Due__c"] - s["paid"], 2)
    s["Status__c"] = "Paid" if bal <= 0 else ("Past Due" if s["Due_Date__c"] < AS_OF else "Open")

# ---- promises (60): 32 Kept, 18 Broken, 8 Active, 2 Pending Approval
promises = []
def oldest_unpaid(a): return next(s for s in by_acc[a] if s["Status__c"] == "Past Due")
delinq = [a for a in bucket_of]
active_accs = rng.sample(BUCKETS["1-30"][0] + [x for x in BUCKETS["31-60"][0] if x not in MISMATCH], 8)
for a in active_accs:
    s = oldest_unpaid(a)
    promises.append(dict(acc=a, rel=s["Legacy_Id__c"], date=AS_OF + timedelta(days=rng.randint(2, 12)),
                         amt=round(s["Amount_Due__c"] - s["paid"], 2), rec=0, status="Active"))
for a in rng.sample(BUCKETS["61-90"][0], 2):
    s = oldest_unpaid(a)
    promises.append(dict(acc=a, rel=s["Legacy_Id__c"], date=AS_OF + timedelta(days=rng.randint(40, 55)),
                         amt=round(s["Amount_Due__c"] - s["paid"], 2), rec=0, status="Pending Approval"))
broken_accs = [a for a in BROKEN_CLUSTER for _ in range(3)] + rng.sample([x for x in delinq if x not in BROKEN_CLUSTER], 6)
for i, a in enumerate(broken_accs):
    s = oldest_unpaid(a)
    window = (5, 85) if i < 12 else (5, 120)
    pdate = AS_OF - timedelta(days=rng.randint(*window))
    amt = s["Amount_Due__c"]
    promises.append(dict(acc=a, rel=s["Legacy_Id__c"], date=pdate, amt=amt,
                         rec=round(amt * rng.choice([0, 0, 0.3, 0.5]), 2), status="Broken"))
# kept: late-but-paid statements; move that payment late and promise just before it
paid_pool = [s for s in stmts if s["Status__c"] == "Paid" and s["Due_Date__c"] < AS_OF - timedelta(days=40)]
for k, s in enumerate(rng.sample(paid_pool, 32)):
    late = s["Due_Date__c"] + timedelta(days=rng.randint(10, 25))
    for p in pays:
        if p["Billing_Statement__r.Legacy_Id__c"] == s["Legacy_Id__c"]:
            p["Payment_Date__c"] = min(late, AS_OF).isoformat()
    promises.append(dict(acc=s["acc"], rel=None if k < 5 else s["Legacy_Id__c"],
                         date=min(late, AS_OF) - timedelta(days=rng.randint(0, 2)),
                         amt=s["Amount_Due__c"], rec=s["Amount_Due__c"], status="Kept"))

# ---- adjustments (12), same mix as the original seed
ADJ = [(28,"Goodwill Credit","Posted",120),(67,"Goodwill Credit","Posted",180),(58,"Goodwill Credit","Approved",120),
       (11,"Goodwill Credit","Rejected",180),(1,"Goodwill Credit","Pending Approval",180),(9,"Goodwill Credit","Approved",180),
       (21,"Billing Correction","Posted",120),(26,"Goodwill Credit","Approved",180),(53,"Goodwill Credit","Approved",45),
       (30,"Goodwill Credit","Posted",420),(87,"Billing Correction","Posted",250),(3,"Production Guarantee","Pending Approval",120)]
adjs = []
for a, t, st, amt in ADJ:
    s = rng.choice(by_acc[a])
    adjs.append({"Account__r.Legacy_Id__c": acc(a), "Billing_Statement__r.Legacy_Id__c": s["Legacy_Id__c"],
                 "Type__c": t, "Status__c": st, "Amount__c": f"{amt:.2f}",
                 "Posted_Date__c": (AS_OF - timedelta(days=rng.randint(10, 80))).isoformat() if st == "Posted" else "",
                 "Rejection_Reason__c": "Credit exceeds policy for a first-time request" if st == "Rejected" else ""})

# ---- accounts
for a in range(1, 89):
    b = bucket_of.get(a, (None,))[0]
    if b is None or a in MISMATCH: status = "Current"
    elif b == "90+": status = "Default Review"
    else: status = "Delinquent"
    broken90 = sum(1 for p in promises if p["acc"] == a and p["status"] == "Broken" and p["date"] >= AS_OF - timedelta(days=90))
    thr = (AS_OF - timedelta(days=dpd_target[a] - 90)).isoformat() if b == "90+" else "#N/A"
    accounts.append({"Legacy_Id__c": acc(a), "Account_Status__c": status, "Broken_Promises_90d__c": broken90,
                     "Collection_Hold_Until__c": "#N/A", "Threshold_Crossed_Date__c": thr})

def write(name, rows, fields):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader()
        for r in rows: w.writerow({k: r[k] for k in fields})

write("01_statements.csv", [{"Legacy_Id__c": s["Legacy_Id__c"], "Account__r.Legacy_Id__c": acc(s["acc"]),
      "Service_Contract__r.Legacy_Id__c": svc(s["acc"]), "Statement_Date__c": s["Statement_Date__c"].isoformat(),
      "Due_Date__c": s["Due_Date__c"].isoformat(), "Amount_Due__c": f'{s["Amount_Due__c"]:.2f}', "Status__c": s["Status__c"]}
      for s in stmts], ["Legacy_Id__c","Account__r.Legacy_Id__c","Service_Contract__r.Legacy_Id__c",
      "Statement_Date__c","Due_Date__c","Amount_Due__c","Status__c"])
write("02_payments.csv", pays, ["Billing_Statement__r.Legacy_Id__c","Amount__c","Payment_Date__c","Method__c","External_Reference__c"])
write("03_promises.csv", [{"Account__r.Legacy_Id__c": acc(p["acc"]), "Related_Statement__r.Legacy_Id__c": p["rel"] or "",
      "Promise_Date__c": p["date"].isoformat(), "Promise_Amount__c": f'{p["amt"]:.2f}', "Amount_Received__c": f'{p["rec"]:.2f}',
      "Status__c": p["status"]} for p in promises],
      ["Account__r.Legacy_Id__c","Related_Statement__r.Legacy_Id__c","Promise_Date__c","Promise_Amount__c","Amount_Received__c","Status__c"])
write("04_adjustments.csv", adjs, ["Account__r.Legacy_Id__c","Billing_Statement__r.Legacy_Id__c","Type__c","Status__c","Amount__c","Posted_Date__c","Rejection_Reason__c"])
write("05_service_contracts.csv", svcs, ["Legacy_Id__c","Activation_Date__c","First_Due_Date__c"])
write("06_accounts.csv", accounts, ["Legacy_Id__c","Account_Status__c","Broken_Promises_90d__c","Collection_Hold_Until__c","Threshold_Crossed_Date__c"])

# ---- self-check
from collections import Counter
def dpd(a):
    pd = [s for s in by_acc[a] if s["Status__c"] == "Past Due"]
    return (AS_OF - min(s["Due_Date__c"] for s in pd)).days if pd else 0
def bk(d): return "Current" if d == 0 else "1-30" if d <= 30 else "31-60" if d <= 60 else "61-90" if d <= 90 else "90+"
print("as of", AS_OF, "| statements", len(stmts), "| payments", len(pays), "| promises", len(promises), "| adjustments", len(adjs))
print("buckets", dict(Counter(bk(dpd(a)) for a in range(1, 89))))
print("promise status", dict(Counter(p["status"] for p in promises)), "| orphans", sum(1 for p in promises if not p["rel"]))
print("future payments", sum(1 for p in pays if p["Payment_Date__c"] > AS_OF.isoformat()),
      "| bad stmt dates", sum(1 for s in stmts if s["Due_Date__c"] < s["Statement_Date__c"]))
print("mismatch accounts", [(acc(a), bk(dpd(a))) for a in sorted(MISMATCH)])
