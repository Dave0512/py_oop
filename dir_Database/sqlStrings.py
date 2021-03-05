

headLieferanten = """SELECT TOP (5) [LieferantenNr]
      ,[AGKALieferanten_Lieferant]
      ,[MiiLieferantGlobal]
      ,[AGKAMED_Langname]
      ,[Finale_UStID]
      ,[tbl_index]
  FROM [Vorlauf_DB].[dbo].[tbl_lieferanten]"""


sql_gui_tab_hcsr_import_erfolgreich = """ IF (EXISTS(
    SELECT *
    FROM Vorlauf_DB.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = 'hcsr'
    ))
    BEGIN
		SELECT DISTINCT [L_Quelle_Name_MUSS_FELD_]
				,[_DateiName_]
		,COUNT(*) Anzahl_Datensätze_je_Lieferant
		,CAST(_date_inload_ as date) Einladedatum
		FROM [Vorlauf_DB].[dbo].[hcsr]
		WHERE CAST(_date_inload_ as date) =  CAST(GETDATE() AS DATE)
		and [L_Quelle_Name_MUSS_FELD_] is not null
		GROUP BY [L_Quelle_Name_MUSS_FELD_], [_DateiName_], _date_inload_
		ORDER BY Einladedatum DESC, Anzahl_Datensätze_je_Lieferant DESC 
	END
ELSE
	BEGIN
		PRINT 'Nicht vorhanden'
	END"""

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
	where _prio_flag_ = '1' 
	and CATNAME like 'eCl@ss' 
	and [CATLEVEL1] not like '%Lief%'
	and CATCODE is not null
	or [CATCODE] = '3410%'
	or [CATCODE] = '3414%'
	or [CATCODE] = '3415%'
	or [CATCODE] = '3418%'
	or [CATCODE] = '3419%'
	or [CATCODE] = '3421%'
	or [CATCODE] = '3422%'
	or [CATCODE] = '3423%'
	or [CATCODE] = '3424%'
	or [CATCODE] = '3425%'
	or [CATCODE] = '3429%'
	or [CATCODE] = '3432%'
	or [CATCODE] = '3433%'
	or [CATCODE] = '3435%'
	or [CATCODE] = '3436%'
	or [CATCODE] = '3437%'
	or [CATCODE] = '3438%'
	or [CATCODE] = '3441%'
	or [CATCODE] = '3442%'
	or [CATCODE] = '3459%'
	or [CATCODE] = '34260703'
	or [CATCODE] = '34260704'
	or [CATCODE] = '34260705'
	or [CATCODE] = '34270112'
	or [CATCODE] = '34090100'
	or [CATCODE] = '34090101'
	or [CATCODE] = '34090102'
	or [CATCODE] = '34090103'
	or [CATCODE] = '34090104'
	or [CATCODE] = '34090190'
	or [CATCODE] = '34090191'
	or [CATCODE] = '34090192'
	or [CATCODE] = '34090200'
	or [CATCODE] = '34090201'
	or [CATCODE] = '34090202'
	or [CATCODE] = '34090203'
	or [CATCODE] = '34090204'
	or [CATCODE] = '34090205'
	or [CATCODE] = '34090290'
	or [CATCODE] = '34090291'
	or [CATCODE] = '34090292'
	or [CATCODE] = '34090300'
	or [CATCODE] = '34090301'
	or [CATCODE] = '34090302'
	or [CATCODE] = '34090390'
	or [CATCODE] = '34090391'
	or [CATCODE] = '34090392'
	or [CATCODE] = '34090400'
	or [CATCODE] = '34090401'
	or [CATCODE] = '34090402'
	or [CATCODE] = '34090490'
	or [CATCODE] = '34090491'
	or [CATCODE] = '34090492'
	or [CATCODE] = '34090500'
	or [CATCODE] = '34090703'
				) as subqueryghxKateclass
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
		,cast(ctePreisstufen.AnzahlPreisstufen as float) / CAST(
				(select COUNT(*) anzahl_art_relevant
				from (
				select SUPPLIERNAME
				,_artikel_key_
				from [Vorlauf_DB].[dbo].[tbl_ghx_kataloge_roh]
				where _prio_flag_ = '1') as subqueryPrSt) as float) as 'Anzahl aktive Preisstufen %'
		,cteArtikel.AnzahlArtikel 'Anzahl aktive Artikel'
		,cast(cteArtikel.AnzahlArtikel as float) / CAST(
				(select COUNT(*) anzahl_art_relevant
				from (select SUPPLIERNAME
					,CATNAME
					,_artikel_key_
					from [Vorlauf_DB].[dbo].[tbl_ghx_kataloge_roh]
					where _prio_flag_ = '1') as subqueryArt)  as float) as 'Anzahl aktive Artikel %'
		,cteGtin.AnzahlGtin 'Anzahl aktive GTIN'
		,cast(cteGtin.AnzahlGtin as float) / CAST(
				(select COUNT(*) anzahl_gtin_relevant
				from (
				select SUPPLIERNAME
				,_artikel_key_
				from [Vorlauf_DB].[dbo].[tbl_ghx_kataloge_roh]
				where _prio_flag_ = '1') as subqueryPrSt) as float) as 'Anzahl aktive GTIN %'
		,cteEclass.AnzahlEclass as 'Anzahl aktive ecl@ss'
		,cast(cteEclass.AnzahlEclass as float) / cast((
			select COUNT(*) anzahl_eclass_relevant
			from (select SUPPLIERNAME
				,CATNAME
				,_artikel_key_
				from [Vorlauf_DB].[dbo].[tbl_ghx_kataloge_roh]
				where _prio_flag_ = '1' and CATNAME like 'eCl@ss' and [CATLEVEL1] not like '%Lief%'
				  and CATCODE is not null
					or [CATCODE] = '3410%'
					or [CATCODE] = '3414%'
					or [CATCODE] = '3415%'
					or [CATCODE] = '3418%'
					or [CATCODE] = '3419%'
					or [CATCODE] = '3421%'
					or [CATCODE] = '3422%'
					or [CATCODE] = '3423%'
					or [CATCODE] = '3424%'
					or [CATCODE] = '3425%'
					or [CATCODE] = '3429%'
					or [CATCODE] = '3432%'
					or [CATCODE] = '3433%'
					or [CATCODE] = '3435%'
					or [CATCODE] = '3436%'
					or [CATCODE] = '3437%'
					or [CATCODE] = '3438%'
					or [CATCODE] = '3441%'
					or [CATCODE] = '3442%'
					or [CATCODE] = '3459%'
					or [CATCODE] = '34260703'
					or [CATCODE] = '34260704'
					or [CATCODE] = '34260705'
					or [CATCODE] = '34270112'
					or [CATCODE] = '34090100'
					or [CATCODE] = '34090101'
					or [CATCODE] = '34090102'
					or [CATCODE] = '34090103'
					or [CATCODE] = '34090104'
					or [CATCODE] = '34090190'
					or [CATCODE] = '34090191'
					or [CATCODE] = '34090192'
					or [CATCODE] = '34090200'
					or [CATCODE] = '34090201'
					or [CATCODE] = '34090202'
					or [CATCODE] = '34090203'
					or [CATCODE] = '34090204'
					or [CATCODE] = '34090205'
					or [CATCODE] = '34090290'
					or [CATCODE] = '34090291'
					or [CATCODE] = '34090292'
					or [CATCODE] = '34090300'
					or [CATCODE] = '34090301'
					or [CATCODE] = '34090302'
					or [CATCODE] = '34090390'
					or [CATCODE] = '34090391'
					or [CATCODE] = '34090392'
					or [CATCODE] = '34090400'
					or [CATCODE] = '34090401'
					or [CATCODE] = '34090402'
					or [CATCODE] = '34090490'
					or [CATCODE] = '34090491'
					or [CATCODE] = '34090492'
					or [CATCODE] = '34090500'
					or [CATCODE] = '34090703'
				) as subqueryghxKateclass
)	as float) as 'Anzahl aktive ecl@ss in % (Covin 207)'
  from ctePreisstufen
  left join cteArtikel
  on cteArtikel.SUPPLIERNAME = ctePreisstufen.SUPPLIERNAME
  left join cteGtin
  on cteArtikel.SUPPLIERNAME = cteGtin.SUPPLIERNAME
  left join cteEclass 
  on cteArtikel.SUPPLIERNAME = cteEclass.SUPPLIERNAME
  right join cteLiefGlobalTPShort
  on cteArtikel.SUPPLIERNAME = cteLiefGlobalTPShort.SUPPLIERNAME
  order by AnzahlEclass desc

"""

sql_abruf_vorh_hcsr_dateien = """
IF (EXISTS(
    SELECT *
    FROM Vorlauf_DB.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = 'hcsrKopfdaten'
    ))
BEGIN

SELECT [_LieferantCompKey_]
  FROM [Vorlauf_DB].[dbo].[hcsrKopfdaten]
  GROUP BY [_LieferantCompKey_]
END

ELSE
BEGIN
PRINT 'Tabelle nicht vorhanden'
END
"""