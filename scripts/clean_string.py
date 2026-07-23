import re

#string = "₹33.8 Lac sqft"
#print(string)
#clean_price_string = re.sub(r'₹| LAC | Cr | per |sqft', '', string, flags=re.IGNORECASE)

#print(clean_price_string)
def clean_string(string):
    if not string:
        return ""

    value = string.strip()
    if not value:
        return ""


    # Convert lac/lakh and cr/crore values into raw rupee numbers first.
    units = re.search(r"(?P<number>[\d.]+)\s*(?P<unit>Lac|Cr)\b", value, flags=re.IGNORECASE)
    if units:
        number = float(units.group("number"))
        unit = units.group("unit").lower()
        multiplier = 100000 if unit in ("lac") else 10000000
        amount = number * multiplier
        return int(round(amount))
        #return str((amount) if amount.is_integer() else amount)

    cleaned_price_string = re.sub(
        r"[₹,]|\s*(?:per|sqft|sq\.ft|ft)\b",
        "",
        value,
        flags=re.IGNORECASE,
    )
    if cleaned_price_string:
        try:
            return int(cleaned_price_string)
        except ValueError:
            return None
    return None
    #return int((cleaned_price_string))
#cleaned_string = clean_string(string)
#print(cleaned_string)