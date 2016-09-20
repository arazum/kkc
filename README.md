# KKC

## Ukratko

Program scrapea http://www.intratext.com/IXT/SCR0001/_INDEX.HTM i sintetizira latex kod iz kojeg se stvara odgovarajući PDF.

## Upotreba

Potreban <tt>latexmk</tt> kako bi stvaranje pdf-a radilo (posljednji korak <tt>make</tt> skripte). Konačni rezultat izvođenja nalazi se u datoteci <tt>output.pdf</tt>.

### Prva upotreba

Pokreni skripte ovim redoslijedom:

1. <tt>./download</tt>
2. <tt>./patch</tt>
3. <tt>./make</tt>

### Uobičajena upotreba

Samo skripta <tt>make</tt> nakon izmjena u <tt>parse.py</tt> ili <tt>cat.py</tt>.

### Ručne izmjene izvora

Ručne izmjene izvora rade se u direktoriju <tt>html</tt>. Nakon toga mora se pokrenuti <tt>capture</tt> i u commitu također uključiti <tt>manual.diff</tt>. Tada drugi mogu ažurirati svoj <tt>html</tt> direktorij upotrebom skripte <tt>patch</tt>.
