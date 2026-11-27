# Kèo đã chấm tuần 23–29/11 (C1 25–26/11, EL 27/11): (giải, ngày, nhà, khách, [(kèo, odds, tier, kết quả, ưu tiên, TOP)])
# kết quả: W thắng, L thua, H hoàn, HW thắng nửa, HL thua nửa
def b(s):
    out=[]
    for x in s.split(';'):
        p=[y.strip() for y in x.split('|')]
        out.append(dict(keo=p[0],odds=float(p[1]),tier=p[2],res=p[3],pr=('P' in p[4:]) or any(y.startswith('P') for y in p[4:]),top='T' in p[4:],cplus='C+' in p[4:]))
    return out
M=[
('C1','25/11','Bodø/Glimt','LASK',b("LASK +1,5|2.00|B|W|P|T;Xỉu 3,5 bàn|2.32|B|W|P;Xỉu 10 góc|1.82|C|W;Xỉu 4,5 góc H1|1.92|C|W;Tài 3,5 thẻ|2.14|C|L")),
('C1','25/11','Galatasaray','Aston Villa',b("Galatasaray +0,25|2.08|C|W;Xỉu 3,5 bàn|1.61|B|W|P;Tài 9,5 góc|1.90|B|L|P|T;Tài 4,5 góc H1|1.90|C|L;Tài 4,5 thẻ|1.78|C|W")),
('C1','25/11','Arsenal','Dortmund',b("Dortmund +1,5|1.65|B|W|P;Xỉu 2,5 bàn|2.16|C|W;Tài 9,5 góc|2.09|B|W|P;Xỉu 4,5 góc H1|1.68|C|L;Tài 3,5 thẻ|2.31|B|L")),
('C1','25/11','Como','AEK',b("Como -1,5|1.72|C|L|P;Xỉu 3,5 bàn|2.00|C|W;Xỉu 9,5 góc|1.83|C|W;Xỉu 4,5 góc H1|1.72|C|W;Xỉu 3,5 thẻ|1.53|B|L|P")),
('C1','25/11','Feyenoord','Porto',b("Porto -0,25|1.83|C|W|P;Tài 3 bàn|2.00|C|L|P;Xỉu 9,5 góc|1.82|C|L;Xỉu 4,5 góc H1|1.71|C|W;Xỉu 4,5 thẻ|1.55|C|L")),
('C1','25/11','Man City','Napoli',b("Napoli +1,5|2.16|B|W|P;Xỉu 3,5 bàn|2.01|C|L;Tài 9,5 góc|1.83|A|W|P|T;Tài 4,5 góc H1|1.90|C|W;Tài 3,5 thẻ|2.13|B|L")),
('C1','25/11','RB Leipzig','Lens',b("RB Leipzig -1,5|1.96|B|W|P;Tài 3,5 bàn|1.72|C|W;Xỉu 10 góc|1.93|C|L;Xỉu 4,5 góc H1|1.93|C|W;Xỉu 3,5 thẻ|1.75|C|L|P")),
('C1','25/11','Real Madrid','PSV',b("PSV +2,5|1.97|B|L|P|T;Xỉu 4,5 bàn|1.90|C|L|P;Tài 10,5 góc|1.96|C|L;Xỉu 4,5 góc H1|1.97|C|W;Xỉu 3,5 thẻ|1.50|C|L")),
('C1','25/11','Slovan Bratislava','Betis',b("Slovan +1,5|2.10|C|L|P;Xỉu 3,5 bàn|1.88|B|W|P;Tài 9,5 góc|1.84|C|L;Tài 4,5 góc H1|1.87|C|L;Xỉu 4,5 thẻ|1.56|C|W")),
('C1','26/11','Sabah','Barcelona',b("Sabah +3|2.06|B|H|P|T;Xỉu 4,5 bàn|2.01|B|L;Xỉu 9,5 góc|1.85|C|L;Tài 4,5 góc H1|1.97|C|L;Tài 3 thẻ|1.92|B|L|P|T")),
('C1','26/11','Slavia Praha','Villarreal',b("Slavia +0,5|1.65|B|L|P;Tài 2,5 bàn|1.52|C|L;Tài 9,5 góc|1.77|B|W;Tài 4,5 góc H1|1.86|B|W|P;Tài 4 thẻ|2.02|B|W")),
('C1','26/11','Atlético','Viking',b("Viking +2,5|2.00|B|W|P;Xỉu 3,5 bàn|2.20|B|W;Xỉu 10,5 góc|1.76|C|W;Xỉu 4,5 góc H1|1.95|B|W;Tài 3,5 thẻ|2.62|A|L|P")),
('C1','26/11','Club Brugge','Liverpool',b("Brugge +1|1.83|B|L;Tài 3,5 bàn|1.76|C|L;Tài 9,5 góc|1.75|B|W;Tài 4,5 góc H1|1.84|B|W|P|T;Tài 3,5 thẻ|1.88|B|L|P")),
('C1','26/11','Inter','Stuttgart',b("Stuttgart +1,5|1.87|B|L;Xỉu 3,5 bàn|2.10|A|W|P|T;Xỉu 9,5 góc|1.91|C|L;Tài 4,5 góc H1|1.90|B|W|P;Xỉu 3,5 thẻ|1.72|C|W")),
('C1','26/11','Shakhtar','Fenerbahçe',b("Shakhtar 0|2.23|C|L|P;Tài 2,5 bàn|1.77|B|L|P;Xỉu 9,5 góc|1.80|C|W;Tài 4,5 góc H1|2.04|C|L;Tài 4,5 thẻ|2.40|C|L")),
('C1','26/11','Lille','Bayern',b("Lille +1|1.83|B|W|P;Xỉu 2,5 bàn|2.10|C|L;Xỉu 9,5 góc|1.77|C|W;Xỉu 4,5 góc H1|1.71|C|L;Xỉu 3,5 thẻ|1.75|B|W|P")),
('C1','26/11','PSG','Roma',b("Roma +1,5|1.75|C|W|P;Tài 3,5 bàn|1.93|C|W|P;Xỉu 9,5 góc|1.70|C|W;Xỉu 4,5 góc H1|1.67|C|L;Tài 3,5 thẻ|2.55|C|L")),
('C1','26/11','Sporting','Man United',b("Sporting 0|1.93|A|H|P;Tài 2,5 bàn|1.52|C|W;Xỉu 9,5 góc|1.83|B|W|P;Xỉu 4,5 góc H1|1.75|C|W;Tài 3,5 thẻ|1.70|C|W")),
('EL','27/11','Beşiktaş','Hapoel Beer Sheva',b("Hapoel +1,75|1.97|C|W;Xỉu 3,5 bàn|1.86|C|W;Xỉu 9,5 góc|1.75|C|L;Xỉu 4,5 góc H1|1.69|B|L|P|T;Tài 4 thẻ|1.99|C|W")),
('EL','27/11','Celta Vigo','Bournemouth',b("Bournemouth -0,25|1.85|C|W|C+;Tài 2,5 bàn|1.93|C|W;Xỉu 9,5 góc|1.70|B|L|P;Xỉu 4,5 góc H1|1.62|B|W|P;Tài 4 thẻ|1.94|C|W")),
('EL','27/11','Dinamo Zagreb','Leverkusen',b("Dinamo +0,75|2.01|C|L;Tài 3,25 bàn|2.00|C|L;Xỉu 9,5 góc|1.86|B|L|P;Xỉu 4,5 góc H1|1.71|C|L;Tài 3 thẻ|1.90|C|W")),
('EL','27/11','Marseille','Levski Sofia',b("Levski +1,5|1.89|C|W;Xỉu 3 bàn|1.89|C|W;Xỉu 9 góc|1.75|B|W|P;Xỉu 4,5 góc H1|1.56|C|W;Tài 4 thẻ|1.97|C|L")),
('EL','27/11','Olympiacos','Milan',b("Olympiacos 0|2.08|B|L|P;Tài 2,5 bàn|1.84|C|W;Xỉu 9 góc|1.88|C|W;Xỉu 4,5 góc H1|1.62|C|W;Tài 4,5 thẻ|1.96|C|W")),
('EL','27/11','Salzburg','Ararat Armenia',b("Ararat +2,25|1.96|C|HW;Xỉu 3,75 bàn|1.91|C|W;Xỉu 9,5 góc|1.88|C|L;Xỉu 4,5 góc H1|1.74|C|L;Tài 4 thẻ|1.71|C|W")),
('EL','27/11','Union SG','Lech Poznań',b("Lech +1,5|1.88|C|W;Tài 3,25 bàn|1.97|C|W;Xỉu 9,5 góc|1.76|C|W;Xỉu 4,5 góc H1|1.75|C|W|C+;Tài 4 thẻ|1.98|C|W")),
('EL','27/11','Viktoria Plzeň','Benfica',b("Plzeň +1,25|1.88|C|W;Xỉu 3,25 bàn|1.97|C|L;Tài 9,5 góc|1.82|B|W|P;Tài 4,5 góc H1|1.97|B|W|P|T;Tài 3,5 thẻ|1.67|C|L")),
('EL','27/11','Crystal Palace','Real Sociedad',b("Real Sociedad +0,5|1.83|B|L|P;Tài 3 bàn|1.89|C|H|C+;Tài 9,5 góc|1.86|B|L|P;Tài 4,5 góc H1|1.98|C|L;Xỉu 4,5 thẻ|1.87|C|L")),
('EL','27/11','Ferencváros','Celje',b("Celje +1,5|1.85|C|W;Tài 3 bàn|1.87|C|L;Tài 9,5 góc|1.80|C|L;Tài 4,5 góc H1|1.95|C|L;Tài 3,5 thẻ|1.96|C|L")),
('EL','27/11','Hoffenheim','Sturm Graz',b("Sturm +1,5|2.02|B|L|P;Xỉu 3,5 bàn|1.87|B|L|P;Tài 10,5 góc|1.94|C|W;Xỉu 4,5 góc H1|1.96|C|L;Tài 3,5 thẻ|1.70|C|L")),
('EL','27/11','Juventus','Omonia',b("Omonia +2,25|1.83|A|L|P|T;Xỉu 3,5 bàn|1.87|B|L|P;Xỉu 9,5 góc|1.83|C|W;Xỉu 4,5 góc H1|1.72|C|L;Xỉu 4,5 thẻ|1.47|C|W")),
('EL','27/11','Lyon','Lillestrøm',b("Lillestrøm +2|1.92|C|W;Xỉu 3,5 bàn|1.85|B|W|P;Tài 10,5 góc|1.99|C|W;Tài 4,5 góc H1|1.80|B|W|P;Xỉu 3,5 thẻ|1.80|C|L")),
('EL','27/11','NEC','Rennes',b("NEC +0,25|2.03|C|W;Tài 3,25 bàn|2.03|C|W|C+;Tài 10 góc|1.99|C|L;Tài 4,5 góc H1|1.90|C|L;Tài 3,5 thẻ|1.78|C|W")),
('EL','27/11','OFI Crete','Anderlecht',b("OFI +0,75|1.87|C|L;Xỉu 2,75 bàn|1.97|C|L;Tài 9,5 góc|1.84|C|W;Tài 4,5 góc H1|1.96|C|W;Tài 4,5 thẻ|2.10|C|W")),
('EL','27/11','Sparta Prague','AZ Alkmaar',b("Sparta +0,25|1.88|C|L;Tài 2,75 bàn|1.85|C|W;Xỉu 10 góc|1.80|C|W;Xỉu 4,5 góc H1|1.85|C|W;Xỉu 4,5 thẻ|1.75|C|W")),
('EL','27/11','Sunderland','Jagiellonia',b("Jagiellonia +1,75|1.94|A|W|P|T;Xỉu 3 bàn|1.95|B|W;Xỉu 9,5 góc|1.90|B|L|P;Xỉu 4,5 góc H1|1.76|C|L;Tài 4,5 thẻ|2.45|C|L")),
('EL','27/11','Torreense','Celtic',b("Torreense +0,75|2.08|C|HL;Tài 3 bàn|1.88|C|H;Tài 10 góc|1.83|C|H;Tài 4,5 góc H1|1.82|C|W;Tài 4,5 thẻ|2.40|C|L")),
]
