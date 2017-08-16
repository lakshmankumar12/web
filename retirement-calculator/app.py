from browser import document,alert
from browser.html import TABLE, THEAD, TBODY, TR, TH, TD, P

def insert_table(values):
    document["calculated_table"].clear()
    document["calculated_table_error"].clear()

    if not values:
        document["calculated_table_error"] <= P("Fix the errors")

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

    document["calculated_table"] <= table

def fmts(val):
    return '${:,.2f}'.format(val)

def calculate_values():
    age = int(document['age'].value)
    sustain_age = int(document['till_age'].value)
    returns = float(document['returns'].value)
    inflation = float(document['inflation'].value)
    expenses = int(document['expenses'].value)

    if age < 18 or age > 101:
        return []

    if sustain_age <= age or sustain_age > 101:
        return []

    if returns < 0 or returns > 30:
        return []

    if inflation < 0 or inflation > 30:
        return []

    if expenses < 1 or expenses > 1000000:
        return []

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


def handle_till_age_change(event):
    s_age = int(document['age'].value)
    age = int(document['till_age'].value)
    document['till_age_error'].clear()
    if age < 18 or age > 101:
        document['till_age_error'] <= P("Sustainence Age should be between 18 and 101")
        document['till_age'].focus()
    elif age <= s_age:
        document['till_age_error'] <= P("Sustainence Age should be greater than present age")
        document['till_age'].focus()
    update_table(None)

def verify_int_value(field,error_str,min,max):
    val = int(document[field].value)
    document[field+'_error'].clear()
    if val < min or val > max:
        document[field+'_error'] <= P(error_str+" should be between %d and %d"%(min,max))
        document[field].focus()
    update_table(None)

def verify_float_value(field,error_str,min,max):
    val = float(document[field].value)
    document[field+'_error'].clear()
    if val < min or val > max:
        document[field+'_error'] <= P(error_str+" should be between %.2f and %.2f"%(min,max))
        document[field].focus()
    update_table(None)

def handle_age_change(event):
    verify_int_value('age','Present age',18,101)

def handle_returns_change(event):
    verify_float_value('returns','Returns Percent',0,30)

def handle_inflation_change(event):
    verify_float_value('inflation','Inflation Percent',0,30)

def handle_expenses_change(event):
    verify_int_value('expenses','Monthly Expenses',1,1000000)

def update_table(event):
    values = calculate_values()
    insert_table(values)

document['age'].bind('change',handle_age_change)
document['till_age'].bind('change',handle_till_age_change)
document['returns'].bind('change',handle_returns_change)
document['inflation'].bind('change',handle_inflation_change)
document['expenses'].bind('change',handle_expenses_change)

update_table(None)
