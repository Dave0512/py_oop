

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
AND [L_Quelle_Name_MUSS_FELD_] is not null
GROUP BY [L_Quelle_Name_MUSS_FELD_], [_DateiName_], _date_inload_
ORDER BY Einladedatum DESC, Anzahl_Datensätze_je_Lieferant DESC """

sql_gui_tab_hcsr_import_fehlerhaft = """ select distinct _AusgeschlDateiPfad_
				                        ,CAST(_date_inload_ as date) Einladedatum
FROM [Vorlauf_DB].[dbo].hcsrFilesExcluded
WHERE CAST(_date_inload_ as date) =  CAST(GETDATE() AS DATE)
ORDER BY Einladedatum DESC
"""