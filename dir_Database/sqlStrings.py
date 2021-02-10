

headLieferanten = """SELECT TOP (5) [LieferantenNr]
      ,[AGKALieferanten_Lieferant]
      ,[MiiLieferantGlobal]
      ,[AGKAMED_Langname]
      ,[Finale_UStID]
      ,[tbl_index]
  FROM [Vorlauf_DB].[dbo].[tbl_lieferanten]"""


sql_gui_tab_hcsr_import_erfolgreich = """ select distinct [L_Quelle_Name_MUSS_FELD_]
                                         ,[_DateiName_]
				                         ,COUNT(*) Anzahl_Datensätze_je_Lieferant
				                         ,CAST(_date_inload_ as date) Einladedatum
FROM [Vorlauf_DB].[dbo].[hcsr]
WHERE CAST(_date_inload_ as date) =  CAST(GETDATE() AS DATE)
and [L_Quelle_Name_MUSS_FELD_] is not null
GROUP BY [L_Quelle_Name_MUSS_FELD_], [_DateiName_], _date_inload_
ORDER BY Einladedatum DESC, Anzahl_Datensätze_je_Lieferant DESC """

sql_gui_tab_hcsr_import_fehlerhaft = """ select distinct _AusgeschlDateiPfad_
				                        ,CAST(_date_inload_ as date) Einladedatum
FROM [Vorlauf_DB].[dbo].hcsrFilesExcluded
WHERE CAST(_date_inload_ as date) =  CAST(GETDATE() AS DATE)
ORDER BY Einladedatum DESC
"""

sql_wasserflasche = """

 with cteArtikel as ( 
	  select distinct
	  subqueryghxKatArt.[SUPPLIERNAME]
	 ,COUNT(*) AnzahlArtikel
  FROM (
	select distinct SUPPLIERNAME
			,concat([_computed_normalized_suppliername_]
			,'°'
			,[_computed_normalized_art_nr_]) _Key_Artikel_Normalized_	   
	FROM [Vorlauf_DB].[dbo].[tbl_ghx_kataloge_roh]
	where _prio_flag_ = '1') as subqueryghxKatArt
	group by subqueryghxKatArt.SUPPLIERNAME),

  ctePreisstufen as (
  select subqueryghxKat.SUPPLIERNAME
		,COUNT(*) AnzahlPreisstufen
  from (
	  select SUPPLIERNAME 
			,[_artikel_key_]
	  from [Vorlauf_DB].[dbo].[tbl_ghx_kataloge_roh]
	  where _prio_flag_ = '1') as subqueryghxKat
	  group by subqueryghxKat.SUPPLIERNAME),

  cteGtin as (
  select subqueryghxKatGtin.SUPPLIERNAME
		 ,COUNT(*) AnzahlGtin
  from ( 
	select SUPPLIERNAME
		   ,[_gtin_]
		  from [Vorlauf_DB].[dbo].[tbl_ghx_kataloge_roh]
	  where _prio_flag_ = '1' and [_gtin_] is not null) as subqueryghxKatGtin
  group by subqueryghxKatGtin.SUPPLIERNAME),

  cteEclass as (
  select subqueryghxKateclass.SUPPLIERNAME
		 ,COUNT(*) AnzahlEclass
  from (select SUPPLIERNAME
		,CATNAME
		from [Vorlauf_DB].[dbo].[tbl_ghx_kataloge_roh]
		where _prio_flag_ = '1' and CATNAME like 'eCl@ss' and [CATLEVEL1] not like '%Lief%') as subqueryghxKateclass
  group by subqueryghxKateclass.SUPPLIERNAME
  ),

  cteLiefGlobalTPShort as (
  select Distinct SUPPLIERNAME
		,_LieferantenNameGlobal_
		,TPSHORTNAME
  from [Vorlauf_DB].[dbo].[tbl_ghx_kataloge_roh])

  select cteLiefGlobalTPShort.SUPPLIERNAME 
		,cteLiefGlobalTPShort._LieferantenNameGlobal_ 
		,cteLiefGlobalTPShort.TPSHORTNAME
		,ctePreisstufen.AnzahlPreisstufen 'Anzahl aktive Preisstufen'
		,cteArtikel.AnzahlArtikel 'Anzahl aktive Artikel'
		,cteGtin.AnzahlGtin 'Anzahl aktive GTIN'
		,cteEclass.AnzahlEclass 'Anzahl aktive ecl@ss'

  from ctePreisstufen
  left join cteArtikel
  on cteArtikel.SUPPLIERNAME = ctePreisstufen.SUPPLIERNAME
  left join cteGtin
  on cteArtikel.SUPPLIERNAME = cteGtin.SUPPLIERNAME
  left join cteEclass 
  on cteArtikel.SUPPLIERNAME = cteEclass.SUPPLIERNAME
  right join cteLiefGlobalTPShort
  on cteArtikel.SUPPLIERNAME = cteLiefGlobalTPShort.SUPPLIERNAME
  order by AnzahlArtikel desc
  ,AnzahlPreisstufen desc
  ,AnzahlGtin desc
  ,AnzahlEclass desc
"""