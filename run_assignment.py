#!/usr/bin/env python
# coding: utf-8

# In[75]:


import json
import re


# In[76]:


with open('assignment_1_data/input.json','r') as input_file:
  input_data = json.load(input_file)
  input_file.close()


# In[77]:


with open('assignment_1_data/output.json','r') as output_file:
  output_data = json.load(output_file)
  output_file.close()


# In[78]:


#print(len(input_data))
#print(input_data[0]['input_tokens'])
#print(output_data[0])


# In[80]:


def token_parser(token):
    has_dig = re.search(r"\d",token)
    has_sma = re.search(r"[a-z]",token)
    has_cap = re.search(r"[A-Z]",token)
    has_pun = re.search(r"[^\w\s]",token)
    if(has_pun and not (has_dig or has_sma or has_cap)):
        return 'sil'
    if(has_dig and not (has_cap or has_pun or has_sma)):
        year_check = re.search("^[12][0-9]{3}$",token)
        if(year_check):
            return o_year(token)
        else:
            return o_snumber(token)
        pass
    if(has_dig and has_pun and not(has_sma or has_cap)):
        has_dot = re.findall("\.",token)
        has_dash = re.findall("-",token)
        has_bsl = re.findall("\/",token)
        has_perc = re.findall("%",token)
        has_colon = re.search(":",token)
        if(has_colon):
            return o_snumber(token[:has_colon.span()[0]]) + " " + o_snumber(token[has_colon.span()[1]:])
        if(len(has_perc)>0):
            token = re.sub("%","",token)
        has_oth = re.findall("[^\w\s\.-\/%,]",token)
        if(len(has_bsl)>0):
            #mixed frac
            common_frac = {
                    "1/2":"a half",
                    "1/4":"a quarter"
            }
            ans = ""
            if(re.search(" ",token)):
                token = re.split(" ",token)
                ans = o_snumber(token[0])
                ans += " and "
                if token[1] in common_frac:
                    ans += common_frac[token[1]]
                else:
                    loc = re.search("\/",token[1])
                    ans += o_snumber(token[1][:loc.span()[0]]) + " " + o_snumber(token[1][loc.span()[1]:],True) + "s"
                return ans
            #frac
            if token in common_frac:
                ans += common_frac[token]
            else:
                loc = re.search("\/",token)
                ans += o_snumber(token[:loc.span()[0]]) + " " + o_snumber(token[loc.span()[1]:],True) + "s"
            return ans
            loc = re.search("\/",token)
            return o_snumber(token[:loc.span()[0]]) + " " + o_snumber(token[loc.span()[1]:],True) + "s"
        if(len(has_dot)>0 and len(has_dash)>0):
            value = o_decimal(token)
            if(len(has_perc)>0):
                return "minus " + value + " percent"
            else:
                return "minus " + value
            pass
        if(len(has_dot)>1):
            #IP
            return o_IP(token)
            pass
        if(len(has_dash)>1):
            ddmmyyyy_check = re.search("^([1-9]|0[1-9]|[12][0-9]|3[01])-([1-9]|0[1-9]|1[0-2])-[12][0-9]{3}$",token)
            mmddyyyy_check = re.search("^([1-9]|0[1-9]|1[0-2])-([1-9]|0[1-9]|[12][0-9]|3[01])-[12][0-9]{3}$",token)
            yyyymmdd_check = re.search("^[12][0-9]{3}-([1-9]|0[1-9]|1[0-2])-([1-9]|0[1-9]|[12][0-9]|3[01])$",token)
            if(ddmmyyyy_check):
                return o_ddmmyyyy(token)
            if(mmddyyyy_check):
                return o_mmddyyyy(token)
            if(yyyymmdd_check):
                return o_yyyymmdd(token)
            else:
                return o_IP(token)
            pass
        if(len(has_dash)==1):
            if(token[0] == '-'):
                ans = 'minus '+ o_snumber(token[1:])
            else:
                return o_IP(token)
            if(len(has_perc)>0):
                return ans + " percent"
            else:
                return ans
        if(len(has_dot)==1):
            if(len(has_oth)>0):
                token = re.sub("[^\w\s\.-\/%,]","",token)
            ans = o_decimal(token)
            #curr
            if(len(has_oth)>0): 
                if has_oth[0] == "$":
                    ans += " dollars"
                    return ans
                if has_oth[0] == "€":
                    ans += " euros"
                    return ans
                if has_oth[0] == "₹":
                    ans += " rupees"
                    return ans
                if has_oth[0] == "¥":
                    ans += " yen"
                    return ans
                else:
                    ans += " sil"
                    return ans
            #percent
            if len(has_perc)>0:
                ans += " percent"
                return ans
            return ans
        if(len(has_perc)>0):
            return o_snumber(token) + " percent"
        if(len(has_oth)>0):
            token = re.sub("[^\w\s\.-\/%\,]","",token)
        ans = o_snumber(token)
        #curr
        if(len(has_oth)>0): 
            if has_oth[0] == "$":
                ans += " dollars"
                return ans
            if has_oth[0] == "€":
                ans += " euros"
                return ans
            if has_oth[0] == "₹":
                ans += " rupees"
                return ans
            if has_oth[0] == "¥":
                ans += " yen"
                return ans
            if has_oth[0] == "£":
                ans += " pounds"
                return ans
            else:
                ans += " sil"
                return ans
        return ans
    if(has_dig and (has_sma or has_pun)):
        spl = re.split("[\-\s\,\/]",token)
        newspl = []
        for i in spl:
            if not re.search("^\s*$",i):
                newspl.append(i)
        spl = newspl
        #date
        dd = re.compile("([1-9]|0[1-9]|[12][0-9]|3[01])")
        yr = re.compile("[12][0-9]{3}")
        mon_match={
            "jan":"january",
            "january":"january",
            "feb":"febrary",
            "febrary":"febrary",
            "mar":"march",
            "march":"march",
            "apr":"april",
            "april":"april",
            "may":"may",
            "jun":"june",
            "june":"june",
            "jul":"july",
            "july":"july",
            "aug":"august",
            "august":"august",
            "sep":"september",
            "september":"september",
            "oct":"october",
            "october":"october",
            "nov":"november",
            "november":"november",
            "dec":"december",
            "december":"december"
        }
        has_mon = re.compile("(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|febrary|march|april|may|june|july|august|september|october|november|december)")
        if(has_mon.search(token.lower())):
            if(len(spl) == 3):
                #ddmmyyyy
                if(dd.match(spl[0]) and spl[1].lower() in mon_match and yr.match(spl[2])):
                    return "the " + o_snumber(spl[0],True) + " of " + mon_match[spl[1].lower()] + " " + o_year(spl[2])
                #mmddyyyy
                if(dd.match(spl[1]) and spl[0].lower() in mon_match and yr.match(spl[2])):
                    return mon_match[spl[0].lower()] + " " + o_snumber(spl[1],True) + " " + o_year(spl[2]) 
            if(len(spl) == 2):
                #ddmm
                if(dd.match(spl[0]) and spl[1].lower() in mon_match):
                    return o_snumber(spl[0],True) + " of " + mon_match[spl[1].lower()]
                ##mmyy
                if(spl[0].lower() in mon_match and yr.match(spl[1])):
                    return mon_match[spl[0].lower()]+ " " + o_year(spl[1])#time
        timeam_match = re.compile("(a\.m\.|A\.M\.| AM | am )")
        timepm_match = re.compile("(p\.m\.|P\.M\.| pm | PM )")
        colon_match = re.compile(":")
        cmt = colon_match.search(token)
        tamt = timeam_match.search(token)
        tpmt = timepm_match.search(token)
        if( cmt or  tamt or tpmt):
            token = re.sub("(a\.m\.|A\.M\.| AM | am |p\.m\.|P\.M\.| pm | PM )","",token)
            firstp = token
            seconp = ""
            if(cmt):
                firstp = token[:cmt.span()[0]]
                seconp = token[cmt.span()[1]:]
            ans = o_snumber(firstp)
            if(cmt):
                ans += " " + o_snumber(seconp)
            if(tpmt):
                ans += " p m"
            if(tamt):
                ans += " a m"
            return ans
        #currency
        curr_units = re.compile("[$€₹¥£]")
        if curr_units.search(token):
            has_oth = re.findall("[^\w\s\.-\/%]",spl[0])
            has_dot = re.search("\.",spl[0])
            if(len(spl)>0 and len(has_oth)>0): 
                token = re.sub("[^\w\s\.-\/%]","",spl[0])
                ans= ""
                if(has_dot):
                    ans = o_decimal(spl[0])
                else:
                    ans = o_snumber(spl[0])
                for i in range(1,len(spl)):
                    ans+= " " + spl[i].lower()
                if has_oth[0] == "$":
                    ans += " dollars"
                    return ans
                if has_oth[0] == "€":
                    ans += " euros"
                    return ans
                if has_oth[0] == "₹":
                    ans += " rupees"
                    return ans
                if has_oth[0] == "¥":
                    ans += " yen"
                    return ans
                if has_oth[0] == "£":
                    ans += " pounds"
                else:
                    ans += " sil"
                    return ans
        #units
        has_mult = re.compile(u"(\u00B2|\u00B3)")
        has_unit = re.compile("(PB|GB|MB|KB|mi|km|cm|mm|g|kg|mg|s|hr|m)")
        if(has_mult.search(token) or has_unit.search(token)):
            has_per = re.search("\/",token)
            firstp = token
            seconp = ""
            if(has_per):
                firstp = token[:has_per.span()[0]]
                seconp = token[has_per.span()[1]:]
            multp = {
                "²": "square",
                "³": "cube",
                "2": "square",
                "3": "cube"
            }
            units = {
                "km": "kilometer",
                "cm": "centimeter",
                "mm": "millimeter",
                "g" : "gram",
                "kg": "kilogram",
                "mg": "milligram",
                "s" : "second",
                "hr": "hour",
                "mi": "mile",
                "m" : "meter",
                "KB": "kilobyte",
                "MB": "megabyte",
                "GB": "gigabyte",
                "PB": "peta byte"
            }
            mmt = has_mult.search(firstp)
            mut = has_unit.search(firstp)
            ogfsp = firstp
            firstp = re.sub(u"(\u00B2|\u00B3)","",firstp)
            firstp = re.sub("(PB|KB|MB|GB|mi|m|km|cm|mm|g|kg|mg|s|hr)","",firstp)
            ans = ""
            if(re.search("\.",firstp)):
                #print(firstp)
                ans = o_decimal(firstp)
            else:
                ans = o_snumber(firstp)
            if(mmt):
                ans += " " + multp[ogfsp[mmt.span()[0]:mmt.span()[1]]] 
            if(mut):
                ans += " " + units[ogfsp[mut.span()[0]:mut.span()[1]]] 
                if(not has_per and firstp != '1'):
                    ans+='s'
            if(has_per):
                ans+=' per'
                mmt = has_mult.search(seconp)
                mut = has_unit.search(seconp)
                ogfsp = seconp
                if(mmt):
                    ans += " " + multp[ogfsp[mmt.span()[0]:mmt.span()[1]]] 
                if(mut):
                    ans += " " + units[ogfsp[mut.span()[0]:mut.span()[1]]] 
                    if(firstp != '1'):
                        ans+='s'
            return ans
        spl_suffixes={
                "th":0,
                "st":0,
                "rd":0,
                "nd":0
        }
        if(not re.search("[^\w]",token) and token[-2:] in spl_suffixes):
            return o_snumber(token,True)
        #address
        pass
    if(not has_dig and not has_sma and has_cap):
        #roman
        rom_match = re.compile("^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?$")
        if(rom_match.search(token)):
            return o_roman(token)
        if(has_pun):
            token = re.sub("[^\w\s]","",token)
        token = token.lower()
        ans = token[0]
        for i in range(1,len(token)):
            ans+=" "+token[i]
        return ans
    if(has_sma and has_pun and not has_dig):
        #abbrv
        return "<self>"
    if(not has_dig and not has_pun and has_sma):
        return "<self>"
    if(re.search("\s",token)):
        tokens = re.split("\s",token)
        val = token_parser(tokens[0])
        if val == "<self>" :
            val = tokens[0]
        ans = val
        for t in range(1,len(tokens)):
            val = token_parser(tokens[t])
            if val == "<self>" :
                val = tokens[t]
            ans += " " +val
        return ans
    return "<unk>"


# In[81]:


def o_year(token):
    ans = ""
    splcase = {
        "2000":0,
        "2001":0,
        "2002":0,
        "2003":0,
        "2004":0,
        "2005":0,
        "2006":0,
        "2007":0,
        "2008":0,
        "2009":0,
    }
    m_one = {
        "0":"zero",
        "1":"one",
        "2":"two",
        "3":"three",
        "4":"four",
        "5":"five",
        "6":"six",
        "7":"seven",
        "8":"eight",
        "9":"nine"
    }
    m_ten = {
        "0":"o",
        "10":"ten",
        "11":"eleven",
        "12":"twelve",
        "13":"thirteen",
        "14":"fourteen",
        "15":"fifteen",
        "16":"sixteen",
        "17":"seventeen",
        "18":"eighteen",
        "19":"nineteen",
        "20":"twenty",
        "30":"thirty",
        "40":"forty",
        "50":"fifty",
        "60":"sixty",
        "70":"seventy",
        "80":"eighty",
        "90":"ninety",
        "2":"twenty",
        "3":"thirty",
        "4":"forty",
        "5":"fifty",
        "6":"sixty",
        "7":"seventy",
        "8":"eighty",
        "9":"ninety",
    }
    if token in splcase:
        ans = m_one[token[0]] + " thousand " + m_one[token[3]]
        return ans
    if token[0:2] in m_ten :
        ans += m_ten[token[0:2]]
    else:
        ans += m_ten[token[0]] + " " + m_one[token[1]]
    ans += " "
    if token[2:4] in m_ten :
        ans += m_ten[token[2:4]]
    else:
        ans += m_ten[token[2]] + " " + m_one[token[3]]
    return ans


# In[82]:


def o_number(token,conv=True):
    m_one = {
        "0":"o",
        "1":"one",
        "2":"two",
        "3":"three",
        "4":"four",
        "5":"five",
        "6":"six",
        "7":"seven",
        "8":"eight",
        "9":"nine"
    }
    ans = m_one[token[0]]
    if ans == "o" and len(token) == 1 and conv:
        ans = "zero"
    for i in range(1,len(token)):
        ans += " " + m_one[token[i]]
    return ans
        


# In[83]:




# In[84]:


def o_snumber(token,oth = False):
    token = re.sub("[^\d]","",token)
    m_one = {
        "0":"zero",
        "1":"one",
        "2":"two",
        "3":"three",
        "4":"four",
        "5":"five",
        "6":"six",
        "7":"seven",
        "8":"eight",
        "9":"nine"
    }
    m_ten = {
        "0":"o",
        "10":"ten",
        "11":"eleven",
        "12":"twelve",
        "13":"thirteen",
        "14":"fourteen",
        "15":"fifteen",
        "16":"sixteen",
        "17":"seventeen",
        "18":"eighteen",
        "19":"nineteen",
        "20":"twenty",
        "30":"thirty",
        "40":"forty",
        "50":"fifty",
        "60":"sixty",
        "70":"seventy",
        "80":"eighty",
        "90":"ninety",
        "2":"twenty",
        "3":"thirty",
        "4":"forty",
        "5":"fifty",
        "6":"sixty",
        "7":"seventy",
        "8":"eighty",
        "9":"ninety",
    }
    m_one_oth={
        "0":"zeroth",
        "1":"first",
        "2":"second",
        "3":"third",
        "4":"fourth",
        "5":"fifth",
        "6":"sixth",
        "7":"seventh",
        "8":"eighth",
        "9":"ninth"
    }
    m_ten_oth = {
        "0":"o",
        "10":"tenth",
        "11":"eleventh",
        "12":"twelfth",
        "13":"thirteenth",
        "14":"fourteenth",
        "15":"fifteenth",
        "16":"sixteenth",
        "17":"seventeenth",
        "18":"eighteenth",
        "19":"nineteenht",
        "20":"twentieth",
        "30":"thirtieth",
        "40":"fortieth",
        "50":"fiftieth",
        "60":"sixtieth",
        "70":"seventieth",
        "80":"eightieth",
        "90":"nintieth",
        "2":"twenty",
        "3":"thirty",
        "4":"forty",
        "5":"fifty",
        "6":"sixty",
        "7":"seventy",
        "8":"eighty",
        "9":"ninety",
    }
    ln = len(token)
    ans = ""
    if(ln == 1 or (ln == 2 and token[0] =='0')):
        if(oth):
            ans += m_one_oth[token[ln-1]]
        else:
            ans += m_one[token[ln-1]]
    elif(ln == 2 or (ln == 3 and token[0] == '0')):
        if(ln == 3):
            token = token[1:]
        if(oth):
            if token[0:2] in m_ten:
                ans += m_ten_oth[token[0:2]]
            else:
                ans += m_ten_oth[token[0]] + " " + m_one_oth[token[1]]
        else:
            if token[0:2] in m_ten:
                ans += m_ten[token[0:2]]
            else:
                ans += m_ten[token[0]] + " " + m_one[token[1]]
    elif(ln == 3 or (ln == 4 and token[0] == '0')):
        if(ln == 4):
            token = token [1:]
        ans = m_one[token[0]] + " hundred"
        if token[1:3] != "00" :
            if token[1] == '0':
                ans += " and " + m_one[token[2]]
            else:
                ans += " "
                if(oth):
                    if token[1:3] in m_ten:
                        ans += m_ten_oth[token[1:3]]
                    else:
                        ans += m_ten_oth[token[1]] + " " + m_one_oth[token[2]]
                else:
                    if token[1:3] in m_ten:
                        ans += m_ten[token[1:3]]
                    else:
                        ans += m_ten[token[1]] + " " + m_one[token[2]]
    elif(ln == 4 or (ln == 5 and token[0] == '0')):
        if(ln == 5):
            token = token[1:]
        ans += m_one[token[0]] + " thousand"
        if(token[1] != '0'):
            ans += " "+ m_one[token[1]] + " hundred"
        if(token[2:4] != '00'):
            if token[2] == '0':
                ans += " " + m_one[token[3]]
            else:
                ans += " "
                if(oth):
                    if token[2:4] in m_ten:
                        ans += m_ten_oth[token[2:4]]
                    else:
                        ans += m_ten_oth[token[2]] + " " + m_one_oth[token[3]]
                else:
                    if token[2:4] in m_ten:
                        ans += m_ten[token[2:4]]
                    else:
                        ans += m_ten[token[2]] + " " + m_one[token[3]]
    elif(ln == 5):
        if token[0:2] in m_ten:
            ans += m_ten[token[0:2]]+" thousand"
        else:
            ans += m_ten[token[0]] + " " + m_one[token[1]] + " thousand"
        if(token[2] != '0'):
            ans += " " + m_one[token[2]] + " hundred"
        if(token[3:5] != '00'):
            if token[3] == '0':
                ans += " and " + m_one[token[4]]
            else:
                ans += " "
                if(oth):
                    if token[3:5] in m_ten:
                        ans += m_ten_oth[token[3:5]]
                    else:
                        ans += m_ten_oth[token[3]] + " " + m_one_oth[token[4]]
                else:
                    if token[3:5] in m_ten:
                        ans += m_ten[token[3:5]]
                    else:
                        ans += m_ten[token[3]] + " " + m_one[token[4]]
    return ans


# In[85]:


def o_decimal(token):
    token = re.sub("\s","",token)
    dot = re.search("\.",token)
    ans1 = o_snumber(token[0:dot.span()[0]])
    decm = token[dot.span()[0]+1:]
    #while(len(decm)>1 and decm[len(decm)-1] == '0'):
    #    decm = decm[0:-2]
    ans2 = o_number(decm)
    return ans1 + " point " + ans2


# In[86]:


o_decimal("10.50")


# In[87]:


def o_IP(token):
    has_dot = re.search("\W",token)
    ans = o_number(token[0:has_dot.span()[0]],False)
    token = token[has_dot.span()[1]:]
    has_dot = re.search("\W",token)
    while has_dot:
        if(has_dot.span()[0] > 0):
            ans += " sil " + o_number(token[:has_dot.span()[0]],False)
        token = token[has_dot.span()[1]:]
        has_dot = re.search("\W",token)
    ans += " sil " + o_number(token)
    return ans


# In[88]:


def o_ddmmyyyy(token):
    mon_match={
        "1":"january",
        "2":"febrary",
        "3":"march",
        "4":"april",
        "5":"may",
        "6":"june",
        "7":"july",
        "8":"august",
        "9":"september",
        "10":"october",
        "11":"november",
        "12":"december"
    }
    iden = re.search("[\/,\.\-]",token)
    day = o_snumber(token[:iden.span()[0]],True)
    token = token[iden.span()[1]:]
    if(token[0]=='0'):
        token = token[1:]
    iden = re.search("[\/,\.\-]",token)
    mon = mon_match[token[:iden.span()[0]]]
    token= token[iden.span()[1]:]
    yr = o_year(token)
    ans = day+" of "+mon+" "+yr
    return ans


# In[89]:


def o_mmddyyyy(token):
    mon_match={
        "1":"january",
        "2":"febrary",
        "3":"march",
        "4":"april",
        "5":"may",
        "6":"june",
        "7":"july",
        "8":"august",
        "9":"september",
        "10":"october",
        "11":"november",
        "12":"december"
    }
    if(token[0]=='0'):
        token = token[1:]
    iden = re.search("[\/,\.\-]",token)
    mon = mon_match[token[:iden.span()[0]]]
    token= token[iden.span()[1]:]
    iden = re.search("[\/,\.\-]",token)
    day = o_snumber(token[:iden.span()[0]],True)
    token = token[iden.span()[1]:]
    yr = o_year(token)
    ans = mon+" "+day+" "+yr
    return ans


# In[90]:


def o_yyyymmdd(token):
    mon_match={
        "1":"january",
        "2":"febrary",
        "3":"march",
        "4":"april",
        "5":"may",
        "6":"june",
        "7":"july",
        "8":"august",
        "9":"september",
        "10":"october",
        "11":"november",
        "12":"december"
    }
    iden = re.search("[\/,\.\-]",token)
    yr = o_year(token[:iden.span()[0]])
    token = token[iden.span()[1]:]
    if(token[0]=='0'):
        token = token[1:]
    iden = re.search("[\/,\.\-]",token)
    mon = mon_match[token[:iden.span()[0]]]
    token= token[iden.span()[1]:]
    day = o_snumber(token,True)
    ans = mon+" "+day+" "+yr
    return ans

def o_roman(token):
    rom_char = {
            "I":1,
            "V":5,
            "X":10,
            "L":50,
            "C":100,
            "D":500,
            "M":1000,
            "IV":4,
            "IX":9,
            "XL":40,
            "XC":90,
            "CD":400,
            "CM":900
    }
    i = 0 
    ans = 0
    while i<len(token):
        if i+1<len(token) and token[i:i+2] in rom_char:
            ans+=rom_char[token[i:i+2]]
            i+=2
        else:
            ans+=rom_char[token[i]]
            i+=1
    return o_snumber(str(ans))




# In[92]:


#main
proc_data = []
for i in range(0,len(input_data)):
    ans = []
    for token in input_data[i]['input_tokens']:
        ans.append(token_parser(token))
    entry = {
        "sid" : i,
        "output_tokens":ans
    }
    proc_data.append(entry)

with open('proc.json','w') as proc_file:
    json.dump(proc_data,proc_file,indent=2)



