USE [ou_kash]
GO

/****** Object:  View [dbo].[UserRoles]    Script Date: 12/19/2025 9:43:35 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE  view  [dbo].[UserRoles]

as
select top 10000 * from (
    SELECT UPPER(b.FIRST +'.'+ isnull(b.LAST,'')) as Name, a.PERSON_JOB_ID , 
              CASE
                  WHEN [FUNCTION] ='Mashgiach'  -- and  a.PERSON_JOB_ID in (select distinct ACTUAL_PERSON_JOB_ID
                                                 --                              from visits 
                                                  ---                             where ACTUAL_VISIT_DATE > getdate() - 400 )
                        THEN 'RFR' 
                  WHEN [FUNCTION] ='Rabbinic Coordinator' THEN 'NCRC'
                  WHEN [FUNCTION] ='Ingredient Dept' THEN 'IAR'
                  WHEN [FUNCTION] ='Product Dept' THEN 'PRODUCT'
               END as role
    FROM PERSON_JOB a, PERSON b
    WHERE a.PERSON_ID = b.PERSON_ID
    and  STATUS not in( 'Terminated', 'Leave', 'Deceased') and
        [FUNCTION] in  ('Mashgiach', 'Rabbinic Coordinator', 'Ingredient Dept', 'Product Dept' ) 
    ) A
    where role is not null
    order by Name, role  asc



GO


/****** Object:  View [dbo].[ActiveNCRC]    Script Date: 12/19/2025 9:43:35 AM ******/


CREATE  view  [dbo].[ActiveNCRC]

as
SELECT DISTINCT b.LAST +', '+ isnull(b.FIRST,'') as NCRC, a.PERSON_JOB_ID 
FROM PERSON_JOB a,
PERSON b
WHERE a.PERSON_ID = b.PERSON_ID
AND a.[FUNCTION] = 'Rabbinic Coordinator'


GO



/****** Object:  View [dbo].[ActiveRFR]    Script Date: 12/19/2025 9:43:35 AM ******/

CREATE  view  [dbo].[ActiveRFR]

as

SELECT DISTINCT b.LAST +', '+ isnull(b.FIRST,'') as RFR, a.PERSON_JOB_ID 
FROM PERSON_JOB a,
PERSON b
WHERE a.PERSON_ID = b.PERSON_ID
AND a.[FUNCTION] = 'Mashgiach'
and a.PERSON_JOB_ID in (select distinct ACTUAL_PERSON_JOB_ID
				from visits 
				where ACTUAL_VISIT_DATE > getdate() - 400 )
-- ORDER BY b.LAST +', '+ isnull(b.FIRST,'')


GO