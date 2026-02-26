-- Link SUBMISSION rows to their matching WORKFLOW counterpart (by ExternalAppRef)
UPDATE s
SET s.[WFLinkedApp] = w.[ApplicationID]
FROM [dbo].[WF_Applications] s
JOIN [dbo].[WF_Applications] w
    ON  w.[ExternalAppRef] = s.[ExternalAppRef]
    AND w.[ApplicationType] = 'WORKFLOW'
WHERE s.[ApplicationType] = 'SUBMISSION'
and  s.[WFLinkedApp] = 0;
GO
-- Link WORKFLOW rows to their matching SUBMISSION counterpart (by ExternalAppRef)
UPDATE w
SET w.[WFLinkedApp] = s.[ApplicationID]
FROM [dbo].[WF_Applications] w
JOIN [dbo].[WF_Applications] s
    ON  s.[ExternalAppRef] = w.[ExternalAppRef]
    AND s.[ApplicationType] = 'SUBMISSION'
WHERE w.[ApplicationType] = 'WORKFLOW'
and w.[WFLinkedApp] = 0;
GO
-- Verify results
SELECT 
    [ApplicationID],
    [ExternalAppRef],
    [WFLinkedApp],
    [ApplicationType]
FROM [dbo].[WF_Applications]
WHERE [ApplicationType] = 'SUBMISSION'
ORDER BY [ExternalAppRef];
GO
SELECT 
    [ApplicationID],
    [ExternalAppRef],
    [WFLinkedApp],
    [ApplicationType]
FROM [dbo].[WF_Applications]
WHERE [ApplicationType] = 'WORKFLOW'
ORDER BY [ExternalAppRef];
GO