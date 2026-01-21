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

SELECT top  10000
  p.PERSON_ID,
  p.KashLogIn          AS userName,
  pc.BusinessEmail,
  p.LAST + ', ' + p.FIRST AS fullName,

  -- per-user count of NCRC assignments
  --ra.userSelected,

  -- total applications (computed once)
  --t.totalApp,

  -- percent of total applications (userSelected / totalApp * 100)
  ROUND(
    CAST(ra.userSelected AS FLOAT) / NULLIF(CAST(t.totalApp AS FLOAT), 0) * 100.0,
    2
  ) AS pct_of_total_apps,
  ROUND(
    CAST(ra.userSelected AS FLOAT) / NULLIF(CAST(t1.totalApp AS FLOAT), 0) * 100.0,
    2
  ) AS pct_of_total_apps_at_work

  -- total NCRC assignments (computed once)
  --total_ncrc.total_ncrc

  -- percent of all NCRC assignments (userSelected / total NCRC assignments * 100)


FROM PERSON_TB p
JOIN PERSON_JOB_TB pj
  ON pj.PERSON_ID = p.PERSON_ID
  AND pj.ACTIVE = 1
  AND pj.[FUNCTION] = 'Mashgiach'
LEFT JOIN PersonContacts pc
  ON pc.Person_ID = p.PERSON_ID

-- per-row count for this user (fast because it references index on RoleAssigment.assignee)
CROSS APPLY (
  SELECT COUNT(*) AS userSelected
  FROM [dashboard].[dbo].[RoleAssigment] ra
  WHERE ra.[assignee] = p.KashLogIn
    AND ra.[Role] = 'RFR'
) ra

-- totals computed once for the whole result set
CROSS JOIN (
  SELECT COUNT(*) AS totalApp
  FROM [dashboard].[dbo].[WF_Applications]
) t

-- totals computed once for the whole result set
CROSS JOIN (
  SELECT COUNT(*) AS totalApp
  FROM [dashboard].[dbo].[WF_Applications] where status not in ('COMPL', 'INC', 'WTH')
) t1

WHERE p.ACTIVE = 1
  AND (p.LAST NOT LIKE 'Z\"L%'        -- preserve your original exclusions
       AND p.LAST NOT LIKE 'z''l%'
       AND p.LAST NOT LIKE 'Reins%'
       AND p.LAST NOT LIKE 'Trans%')
  AND p.KashLogIn IS NOT NULL

--ORDER BY ra.userSelected DESC;  -- optional: largest contributors first
ORDER by fullName ASC

GO

CREATE  view  [dbo].[v_selectNCRC]

as
SELECT top  10000
  p.PERSON_ID,
  p.KashLogIn          AS userName,
  pc.BusinessEmail,
  p.LAST + ', ' + p.FIRST AS fullName,

  -- per-user count of NCRC assignments
  --ra.userSelected,

  -- total applications (computed once)
  --t.totalApp,

  -- percent of total applications (userSelected / totalApp * 100)
  ROUND(
    CAST(ra.userSelected AS FLOAT) / NULLIF(CAST(t.totalApp AS FLOAT), 0) * 100.0,
    2
  ) AS pct_of_total_apps,

    -- percent of total applications at work (userSelected / totalApp * 100)
  ROUND(
    CAST(ra.userSelected AS FLOAT) / NULLIF(CAST(t1.totalApp AS FLOAT), 0) * 100.0,
    2
  ) AS pct_of_total_apps_at_work

  -- total NCRC assignments (computed once)
  --total_ncrc.total_ncrc

  -- percent of all NCRC assignments (userSelected / total NCRC assignments * 100)


FROM PERSON_TB p
JOIN PERSON_JOB_TB pj
  ON pj.PERSON_ID = p.PERSON_ID
  AND pj.ACTIVE = 1
  AND pj.[FUNCTION] = 'NCRC'
LEFT JOIN PersonContacts pc
  ON pc.Person_ID = p.PERSON_ID

-- per-row count for this user (fast because it references index on RoleAssigment.assignee)
CROSS APPLY (
  SELECT COUNT(*) AS userSelected
  FROM [dashboard].[dbo].[RoleAssigment] ra
  WHERE ra.[assignee] = p.KashLogIn
    AND ra.[Role] = 'NCRC'
) ra

-- totals computed once for the whole result set
CROSS JOIN (
  SELECT COUNT(*) AS totalApp
  FROM [dashboard].[dbo].[WF_Applications]
) t

-- totals computed once for the whole result set
CROSS JOIN (
  SELECT COUNT(*) AS totalApp
  FROM [dashboard].[dbo].[WF_Applications] where status not in ('COMPL', 'INC', 'WTH')
) t1



WHERE p.ACTIVE = 1
  AND (p.LAST NOT LIKE 'Z\"L%'        -- preserve your original exclusions
       AND p.LAST NOT LIKE 'z''l%'
       AND p.LAST NOT LIKE 'Reins%'
       AND p.LAST NOT LIKE 'Trans%')
  AND p.KashLogIn IS NOT NULL

--ORDER BY ra.userSelected DESC;  -- optional: largest contributors first
ORDER by fullName ASC


GO
