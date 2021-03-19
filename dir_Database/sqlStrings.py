

headLieferanten = """SELECT TOP (5) [LieferantenNr]
      ,[AGKALieferanten_Lieferant]
      ,[MiiLieferantGlobal]
      ,[AGKAMED_Langname]
      ,[Finale_UStID]
      ,[tbl_index]
  FROM [Vorlauf_DB].[dbo].[tbl_lieferanten]"""


sql_abruf_vorh_hcsr_dateien_key = """
IF (EXISTS(
    SELECT *
    FROM Vorlauf_DB.INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = 'hcsrKopfdaten'
    ))
    BEGIN

SELECT Distinct
      [_LieferantCompKey_]
  FROM [Vorlauf_DB].[dbo].[hcsrKopfdaten]

	END
ELSE
	BEGIN
		PRINT 'Nicht vorhanden'
	END
"""

sql_gui_tab_hcsr_import_erfolgreich = """ IF (EXISTS(
	SELECT *
	FROM Vorlauf_DB.INFORMATION_SCHEMA.TABLES
	WHERE TABLE_NAME = 'hcsr'
	))
BEGIN
	SELECT DISTINCT [L_Quelle_Name_MUSS_FELD_]
			,[_DateiName_]
	,COUNT(*) Anzahl_Datensätze_je_Lieferant
	,_date_inload_minute_ Einladedatum --,CAST(_date_inload_ as date) Einladedatum
	FROM [Vorlauf_DB].[dbo].[hcsr]
	-- WHERE CAST(_date_inload_ as date) =  CAST(GETDATE() AS DATE)
	WHERE [L_Quelle_Name_MUSS_FELD_] is not null
	GROUP BY [L_Quelle_Name_MUSS_FELD_], [_DateiName_], _date_inload_minute_
	ORDER BY Einladedatum ASC, [L_Quelle_Name_MUSS_FELD_] ASC 
END
ELSE
BEGIN
	PRINT 'Nicht vorhanden'
END
	"""

sql_gui_tab_hcsr_import_erfolgreich_2 = """
with ctehcsr as (
SELECT DISTINCT [L_Quelle_Name_MUSS_FELD_]
		,[_DateiName_]
,COUNT(*) Anzahl_Datensätze_je_Lieferant
,_date_inload_minute_ Einladedatum --,CAST(_date_inload_ as date) Einladedatum
,sum([Umsatz_MUSS_FELD_]) Umsatz
FROM [Vorlauf_DB].[dbo].[hcsr]
-- WHERE CAST(_date_inload_ as date) =  CAST(GETDATE() AS DATE)
WHERE [L_Quelle_Name_MUSS_FELD_] is not null
GROUP BY [L_Quelle_Name_MUSS_FELD_], [_DateiName_], _date_inload_minute_
--ORDER BY Einladedatum ASC, [L_Quelle_Name_MUSS_FELD_] ASC 
) 
select distinct ctehcsr.* 
,CAST(kopf.datumVon as date) 'Umsatz von'
,CAST(kopf.datumBis as date) 'Umsatz bis'
from ctehcsr
left join hcsrKopfdaten kopf
on ctehcsr._DateiName_ = kopf._DateiName_     
where ctehcsr.[L_Quelle_Name_MUSS_FELD_] like ?
or ctehcsr.[_DateiName_] like ?  
or ctehcsr.Anzahl_Datensätze_je_Lieferant like ?
or ctehcsr.Einladedatum like ?  
or ctehcsr.Umsatz like ? 
or kopf.datumVon like ? 
or kopf.datumBis like ?    
"""

sql_hcsr_details = """
SELECT 
cast(kopf.datumVon as date) 'Umsatz von'
,cast(kopf.datumBis as date) 'Umsatz bis'
,h.[L_Quelle_Name_MUSS_FELD_]
,h.[L_Quelle_IDTyp_Auswahl_MUSS_FELD_]
,h.[L_Quelle_ID_MUSS_FELD_]
,h.[H_Quelle_Name]
,h.[H_Quelle_IDTyp_Auswahl]
,h.[H_Quelle_ID]
,h.[Einrichtung_MUSS_FELD_]
,h.[Organisation_ID_Auswahl_MUSS_FELD_]
,h.[Organisation_ID_MUSS_FELD_]
,h.[L_Art_Nr_MUSS_FELD_]
,h.[L_Art_IDTyp_Auswahl]
,h.[L_Art_ID_MUSS_FELD_]
,h.[H_Art_Nr_MUSS_FELD_]
,h.[H_Art_IDTyp_Auswahl]
,h.[H_Art_ID_MUSS_FELD_]
,h.[L_Art_Txt_MUSS_FELD_]
,h.[L_WGRP_Intern]
,h.[L_WGRP_Merkmale_Intern]
,h.[L_VPE_Auswahl_MUSS_FELD_]
,h.[L_VPE_Menge_MUSS_FELD_]
,h.[Faktor_BASISME_VPE_MUSS_FELD_]
,h.[BASISME_Auswahl_MUSS_FELD_]
,h.[Steuersatz Landescode_MUSS_FELD_]
,h.[Steuersatz_MUSS_FELD_]
,h.[Umsatz_MUSS_FELD_]
,h.[Bonusrelevant_MUSS_FELD_]
,h.[_date_inload_]
,h.[_date_inload_minute_]
,h.[_date_inload_hour_]
,h.[_DateiName_]
,h.[L_Quelle_ID_MUSS_FELD__NORMALIZED]
,h.[L_Quelle_Name_MUSS_FELD__NORMALIZED]
,h.[L_Art_ID_MUSS_FELD__NORMALIZED]
,h.[H_Quelle_ID_NORMALIZED]
,h.[H_Art_Nr_MUSS_FELD__NORMALIZED]
,h.[H_Art_ID_MUSS_FELD__NORMALIZED]
,h.[_prio_flag_]
,h.[_DateiNameCompKey_]
FROM [Vorlauf_DB].[dbo].[hcsr] h
left join hcsrKopfdaten kopf
on h._DateiName_ = kopf._DateiName_ 
where _prio_flag_ = 1
or [L_Quelle_Name_MUSS_FELD_] like ?
or [L_Quelle_IDTyp_Auswahl_MUSS_FELD_] like ?
or [L_Quelle_ID_MUSS_FELD_] like ?
or [H_Quelle_Name] like ?
or [H_Quelle_IDTyp_Auswahl] like ?
or [H_Quelle_ID] like ?
or [Einrichtung_MUSS_FELD_] like ?
or [Organisation_ID_Auswahl_MUSS_FELD_] like ?
or [Organisation_ID_MUSS_FELD_] like ?
or [L_Art_Nr_MUSS_FELD_] like ?
or [L_Art_IDTyp_Auswahl] like ?
or [L_Art_ID_MUSS_FELD_] like ?
or [H_Art_Nr_MUSS_FELD_] like ?
or [H_Art_IDTyp_Auswahl] like ?
or [H_Art_ID_MUSS_FELD_] like ?
or [L_Art_Txt_MUSS_FELD_] like ?
or [L_WGRP_Intern] like ?
or [L_WGRP_Merkmale_Intern] like ?
or [L_VPE_Auswahl_MUSS_FELD_] like ?
or [L_VPE_Menge_MUSS_FELD_] like ?
or [Faktor_BASISME_VPE_MUSS_FELD_] like ?
or [BASISME_Auswahl_MUSS_FELD_] like ?
or [Steuersatz Landescode_MUSS_FELD_] like ?
or [Steuersatz_MUSS_FELD_] like ?
or [Umsatz_MUSS_FELD_] like ?
or [Bonusrelevant_MUSS_FELD_] like ?
or [_date_inload_] like ?
or [_date_inload_minute_] like ?
or [_date_inload_hour_] like ?
or [_DateiName_] like ?
or [L_Quelle_ID_MUSS_FELD__NORMALIZED] like ?
or [L_Quelle_Name_MUSS_FELD__NORMALIZED] like ?
or [L_Art_ID_MUSS_FELD__NORMALIZED] like ?
or [H_Quelle_ID_NORMALIZED] like ?
or [H_Art_Nr_MUSS_FELD__NORMALIZED] like ?
or [H_Art_ID_MUSS_FELD__NORMALIZED] like ?
or [_prio_flag_] like ?
or [_DateiNameCompKey_] like ?
or kopf.datumVon like ? 
or kopf.datumBis like ? 
"""

sql_gui_tab_hcsr_import_fehlerhaft = """ select distinct _AusgeschlDateiPfad_
,_DateiName_
,_FehlerCode_
,CAST(_date_inload_ as date) Einladedatum
FROM [Vorlauf_DB].[dbo].hcsrFilesExcluded hE
where hE._AusgeschlDateiPfad_ like ?
or hE._DateiName_ like ?
or hE._FehlerCode_ like ?
or cast(hE._date_inload_ as date) like ?
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

sql_delete_aus_hcsrEx_in_hcsr_vorhandene_dateien = """
delete
from [Vorlauf_DB].[dbo].[hcsrFilesExcluded]
where substring(right([_AusgeschlDateiPfad_],(CHARINDEX('\',reverse([_AusgeschlDateiPfad_])))),2,LEN([_AusgeschlDateiPfad_]))  =
(select distinct  
		hcsr._DateiName_
from
(SELECT [_AusgeschlDateiPfad_]
		,substring(right([_AusgeschlDateiPfad_],(CHARINDEX('\',reverse([_AusgeschlDateiPfad_])))),2,LEN([_AusgeschlDateiPfad_])) as _DateiName_
		,[_FehlerCode_]
		,[_date_inload_]
	FROM [Vorlauf_DB].[dbo].[hcsrFilesExcluded]) hcsrEx
inner join [Vorlauf_DB].[dbo].[hcsr]
on hcsr.[_DateiName_] = hcsrEx._DateiName_) 
"""

sql_datenModell = """ IF NOT EXISTS (SELECT * FROM dbo.sysobjects
			  WHERE ID = OBJECT_ID(N'[dbo].[hcsrFiles]')
			  AND OBJECTPROPERTY(ID, N'IsUserTable') = 1)
CREATE TABLE Vorlauf_DB.dbo.hcsrFiles (
[_DateiName_] [varchar] (MAX)
,[_date_inload_] [datetime]
,[hcsr_file_id] [int] IDENTITY (1,1) PRIMARY KEY NOT NULL)
"""

sql_add_primary_key = """
    ALTER TABLE [Vorlauf_DB].[dbo].[hcsr]
    ADD tbl_index INT NOT NULL IDENTITY (1,1)
"""

# sql_add_prio_flag_part_1 = """ with cte_1_Anzahl as (select distinct
# [_LieferantCompKey_]
# ,COUNT(*) Anz_Key_Handling_Prio
# FROM [Vorlauf_DB].[dbo].[hcsrKopfdaten]
# group by  [_LieferantCompKey_]),  cte_2_MaxTime as (
# SELECT distinct [_LieferantCompKey_]
# ,MAX(_date_inload_minute_) _aktuellster_inload_
# FROM [Vorlauf_DB].[dbo].[hcsrKopfdaten]
# GROUP BY [_LieferantCompKey_]), cte_3_Case as (
# SELECT distinct kopf.*
# ,CASE WHEN cte_1_Anzahl.Anz_Key_Handling_Prio > 1 
# AND kopf.[_date_inload_minute_] = cte_2_MaxTime._aktuellster_inload_ THEN '1' 
# WHEN cte_1_Anzahl.Anz_Key_Handling_Prio = 1 THEN '1'
# ELSE '0' END AS _prio_flag_	
# FROM [Vorlauf_DB].[dbo].[hcsrKopfdaten] kopf
# JOIN cte_1_Anzahl
# ON cte_1_Anzahl.[_LieferantCompKey_] = kopf._LieferantCompKey_
# JOIN cte_2_MaxTime
# ON cte_2_MaxTime._LieferantCompKey_ = kopf._LieferantCompKey_) """

# sql_add_prio_flag_part_4 = """ UPDATE [Vorlauf_DB].[dbo].[hcsr]
# SET [Vorlauf_DB].[dbo].[hcsr]._prio_flag_ = cte_3_Case._prio_flag_
# FROM cte_3_Case
# RIGHT JOIN [Vorlauf_DB].[dbo].[hcsr] h
# on h._DateiName_ = cte_3_Case._DateiName_ and
# CONVERT(datetime,h._date_inload_minute_,102) between DATEADD(minute,-1,CONVERT(datetime,cte_3_Case.[_date_inload_minute_],102)) and DATEADD(minute,+1,CONVERT(datetime,cte_3_Case.[_date_inload_minute_],102))
# and h.[datei_id_counter] = cte_3_Case.[datei_id_counter] """


sql_stored_proc_add_prio_flag = """ exec PRIO_FLAG; """

sql_add_prio_flag_gesamt = """with cte_1_Anzahl as (select distinct
[_LieferantCompKey_]
,COUNT(*) Anz_Key_Handling_Prio
FROM [Vorlauf_DB].[dbo].[hcsrKopfdaten]
group by  [_LieferantCompKey_]), cte_2_MaxTime as (
SELECT distinct [_LieferantCompKey_]
,MAX(_date_inload_minute_) _aktuellster_inload_
FROM [Vorlauf_DB].[dbo].[hcsrKopfdaten]
GROUP BY [_LieferantCompKey_]), cte_3_Case as (
SELECT distinct kopf.*
,CASE WHEN cte_1_Anzahl.Anz_Key_Handling_Prio > 1 
AND kopf.[_date_inload_minute_] = cte_2_MaxTime._aktuellster_inload_ THEN '1' 
WHEN cte_1_Anzahl.Anz_Key_Handling_Prio = 1 THEN '1'
ELSE '0' END AS _prio_flag_	
FROM [Vorlauf_DB].[dbo].[hcsrKopfdaten] kopf
JOIN cte_1_Anzahl
ON cte_1_Anzahl.[_LieferantCompKey_] = kopf._LieferantCompKey_
JOIN cte_2_MaxTime
ON cte_2_MaxTime._LieferantCompKey_ = kopf._LieferantCompKey_) UPDATE [Vorlauf_DB].[dbo].[hcsr]
SET [Vorlauf_DB].[dbo].[hcsr]._prio_flag_ = cte_3_Case._prio_flag_
FROM cte_3_Case
RIGHT JOIN [Vorlauf_DB].[dbo].[hcsr] h
on h._DateiName_ = cte_3_Case._DateiName_ and
CONVERT(datetime,h._date_inload_minute_,102) between DATEADD(minute,-1,CONVERT(datetime,cte_3_Case.[_date_inload_minute_],102)) and DATEADD(minute,+1,CONVERT(datetime,cte_3_Case.[_date_inload_minute_],102))
and h.[datei_id_counter] = cte_3_Case.[datei_id_counter]
"""


sql_delete_empty_rows = """
                        DELETE FROM {}
                        WHERE 
                                  [TPSHORTNAME] IS NULL OR [TPSHORTNAME] = ''
                              AND [ACTIONCODE] IS NULL OR [TPSHORTNAME] = ''
                              AND [MFRNAME] IS NULL OR [TPSHORTNAME] = ''
                              AND [MFRPARTNUM] IS NULL OR [TPSHORTNAME] = ''
                              AND [SUPPLIERNAME] IS NULL OR [TPSHORTNAME] = ''
                              AND [SUPPLIERPARTNUM] IS NULL OR [TPSHORTNAME] = ''
                              AND [BaseUOM] IS NULL OR [TPSHORTNAME] = ''
                              AND [NOU] IS NULL OR [TPSHORTNAME] = ''
                              AND [UOM] IS NULL OR [TPSHORTNAME] = ''
                        """