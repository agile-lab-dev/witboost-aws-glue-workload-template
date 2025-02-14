import "strings"
let splits = strings.Split(id, ":")
let domain = splits[3]
let majorVersion = splits[5]

#Id:               string & =~"^[a-zA-Z0-9:._\\-]+$"
#ComponentId:      #Id & =~"^urn:dmb:cmp:\(domain):[a-zA-Z0-9_\\-]+:\(majorVersion):[a-zA-Z0-9_\\-]+$"

#OM_Tag: {
	tagFQN:       string
	description?: string | null
	source:       string & =~"(?i)^(Tag|Glossary)$"
	labelType:    string & =~"(?i)^(Manual|Propagated|Automated|Derived)$"
	state:        string & =~"(?i)^(Suggested|Confirmed)$"
	href?:        string | null
}

#GlueJobSpecific: {
    region: string & =~"^(us|eu|ap|sa|ca|me|af)-[a-z]+-\\d+$"
    iamRole: string & =~"^arn:aws:iam::\\d{12}:role/[A-Za-z0-9+=,.@_-]+$"
    scriptName: string
    workerType: string & =~"(?i)^(G.1X|G.2X|G.4X|G.8X)$"
    numberOfWorkers: int & > 0
    executionClass: string & =~"^(STANDARD|FLEX)$"
    storageAreaId: #ComponentId
    timeout: int & > 0
    catalogName: "glue_catalog"
    warehouseLocation: string
}


id:                       #ComponentId
description:              string
name:                     string
fullyQualifiedName?:      null | string
kind:                     string & =~"(?i)^(workload)$"
version:                  string
infrastructureTemplateId: string
useCaseTemplateId?:       null | string
dependsOn?: [...#ComponentId]
readsFrom?: [...#ComponentId]
workloadType?:   string | null
connectionType?: string & =~"(?i)^(housekeeping|datapipeline)$" | null
platform:        string & =~"(?i)^(AWS)$"
technology:      string & =~"(?i)^(Glue)$"
workloadType:    string & =~"(?i)^(batch)$"
connectionType:  string & =~"(?i)^(DataPipeline)$"
tags: [...#OM_Tag]
specific: #GlueJobSpecific