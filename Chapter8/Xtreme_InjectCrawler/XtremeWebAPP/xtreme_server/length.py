List_Vectors =['[A-Za-z0-9]+\' or \'1\' = \'1\' or \'[A-Za-z0-9]+',
'[A-Za-z0-9]+\' or \'a\' = \'a\' or \'[A-Za-z0-9]+',
'[A-Za-z0-9]+\" or \'1\' = \'1\' or \"[A-Za-z0-9]+',
'[A-Za-z0-9]+\" or \'a\' = \'a\' or \"[A-Za-z0-9]+',
'[A-Za-z0-9]+\' or 1 = 1 or \'[A-Za-z0-9]+',
'[A-Za-z0-9]+\" or 1 = 1 or \"[A-Za-z0-9]+',
'[A-Za-z0-9]+\"',
'[A-Za-z0-9]+\'',
'[A-Za-z0-9]+<',
'[A-Za-z0-9]+>',
'&[A-Za-z0-9]+',
'[A-Za-z0-9]+<!--',
'[A-Za-z0-9]+<script>[A-Za-z0-9]+</script>[A-Za-z0-9]+',
'[A-Za-z0-9]+]]>',
'<!\[CDATA\[(<\]\]>script<!\[CDATA\[>\]\]>[A-Za-z0-9]+\(\'[A-Za-z0-9]+\'\)<!\[CDATA\[<\]\]>/script<!\[CDATA\[>){1,2}\]\]>',
'(<!\[CDATA\[%s{1,2}\]\]>)' ,
'(<!\[CDATA\[%s{1,2}\]\]>)' ,
'\<\?xml version=\"1\.0\" encoding=\"ISO-8859-1\"\?\>\<\!DOCTYPE foo \[\<\!ELEMENT foo ANY\>\<\!ENTITY xxe SYSTEM \"([A-Za-z0-9_;:@.,\-\[\]\{\}/\!])+\">]><foo>&xxe;</foo>',
'\';convert:binary-to-string("hello world single")',
'\";convert:binary-to-string("hello world double")',
'\'; (eval([A-Za-z_])*)\(([a-zA-Z0-9_.,\'\"\!\*\&])*\); \' ',
'\"; (eval([A-Za-z_])*)\(([a-zA-Z0-9_.,\'\"\!\*\&])*\); \" '
]

List_vuln=[ "Tautology Attack with single quoted string (numeric)",
        "Tautology Attack with single quoted string (alpha)",
	"Tautology Attack with double quoted string (numeric)",
	"Tautology Attack with double quoted string (alpha)",
	"Tautology Attack with single quoted string (integer)",
	"Tautology Attack with double quoted string (integer)",
        "Special character injection (double quote)",
        "Special character injection (single quote)",
        "Meta character injection (<)",
        "Meta character injection (>)",
        "Meta character injection (&)",
        "Comment injection (<!--)",
        "Tag injection",
        "CDATA injection (]]>)",
	"CDATA injection with script tag",
	"CDATA injection with tautology string (single quote)",
	"CDATA injection with tautology string (double quote)",
	"External entity injection",
    "Convert function Single quote",
    "Convert function double quote",
	"Executable Function injection (single quote)",
	"Executable Function injection (double quote)"
]
Len_List_vect=len(List_Vectors)
print(len((List_Vectors)))
print(len((List_vuln)))
for i in List_Vectors:
    print i
print ("\n\n\n\n\n")
for j in List_vuln:
    print j
