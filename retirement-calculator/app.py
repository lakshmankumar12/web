from browser import document,alert
from browser.html import TABLE, THEAD, TBODY, TR, TH, TD

def insert_table(values):
    table = TABLE()
    table.classList.add("table")
    table.classList.add("table-striped")

    # header row
    headings = ['Year','Start-With','Yearly Exp','Monthly Exp','Left With']
    table <= THEAD(TR(TH(i) for i in headings))

    # table rows
    tbody = TBODY()
    for row in values:
        r = TR()
        for v in row:
            r <= TD(v)
        tbody <= r
    table <= tbody

    document["calculated_table"].clear()
    document["calculated_table"] <= table

def fmts(val):
    return '${:,.2f}'.format(val)

def calculate_values():
    age = int(document['age'].value)
    sustain_age = int(document['till_age'].value)
    returns = float(document['returns'].value)
    inflation = float(document['inflation'].value)
    expenses = int(document['expenses'].value)

    expenses_per_year = [0] * sustain_age
    corpus_at_year = [0] * sustain_age

    expenses_per_year[age]=expenses*12
    inf = 1.0 + (inflation/100.0)
    for i in range(age+1,sustain_age):
        expenses_per_year[i] = expenses_per_year[i-1]*inf

    # let calculate corpus needed at beginning to support year-n and work backwards.

    rr = 1.0 + returns/100.0
    corpus_at_year[sustain_age-1] = expenses_per_year[sustain_age-1]
    prev_corpus = corpus_at_year[sustain_age-1]
    for i in range(sustain_age-2,age-1,-1):
        corpus_at_year[i] = expenses_per_year[i] + (prev_corpus/rr)
        prev_corpus = corpus_at_year[i]

    values = []
    for i in range(age,sustain_age):
        a = (i,fmts(corpus_at_year[i]), fmts(expenses_per_year[i]),
                    fmts(expenses_per_year[i]/12), fmts(corpus_at_year[i]-expenses_per_year[i]))
        values.append(a)
    return values

def update_table(event):
    values = calculate_values()
    insert_table(values)

document['age'].bind('change',update_table)
document['till_age'].bind('change',update_table)
document['returns'].bind('change',update_table)
document['inflation'].bind('change',update_table)
document['expenses'].bind('change',update_table)

update_table(None)
