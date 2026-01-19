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




CREATE  view  [dbo].[v_selectRFR]

as
select
	p.PERSON_ID
	,p.KashLogIn as userName
	,pc.BusinessEmail
	,p.LAST + ', ' + P.FIRST as fullName
from PERSON_TB p
join PERSON_JOB_TB pj on pj.PERSON_ID = p.PERSON_ID and pj.ACTIVE = 1 and pj.[FUNCTION] = 'Mashgiach'
left join PersonContacts pc on pc.Person_ID = p.PERSON_ID 
where p.ACTIVE = 1 and (p.LAST not like 'Z"L%' and p.LAST not like 'z''l%' and p.LAST not like 'Reins%' and p.LAST not like 'Trans%')
and p.KashLogIn is not null

GO

CREATE  view  [dbo].[v_selectNCRC]

as
select
	p.PERSON_ID
	,p.KashLogIn as userName
	,pc.BusinessEmail
	,p.LAST + ', ' + P.FIRST as fullName
from PERSON_TB p
join PERSON_JOB_TB pj on pj.PERSON_ID = p.PERSON_ID and pj.ACTIVE = 1 and pj.[FUNCTION] = 'NCRC'
left join PersonContacts pc on pc.Person_ID = p.PERSON_ID 
where p.ACTIVE = 1 and (p.LAST not like 'Z"L%' and p.LAST not like 'z''l%' and p.LAST not like 'Reins%' and p.LAST not like 'Trans%')
and p.KashLogIn is not null


GO
