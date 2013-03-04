ne_data= open('train.gold','r')
ne_gpe = open('ne_gpe.log','w')
ne_loc = open('ne_loc.log','w')
ne_org = open('ne_org.log','w')

loc_list = set()
gpe_list = set()
ORG_list = set()
for rline in ne_data.readlines():
     if rline.strip():
        entry = rline.split()
        if entry[3]=='B-GPE' or entry[3]=='I-GPE':
            gpe_list.add(entry[1])
        elif entry[3]=='B-LOC' or entry[3]=='I-LOC':
            loc_list.add(entry[1])
        elif entry[3]=='B-ORG' or entry[3]=='I-ORG':
            ORG_list.add(entry[1])

for i in gpe_list:
    ne_gpe.write(i+"\n")

for i in loc_list:
    ne_loc.write(i+"\n")

for i in ORG_list:
    ne_org.write(i+"\n")

ne_data.close()
ne_gpe.close()
ne_loc.close()
ne_org.close()