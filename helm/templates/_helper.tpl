{{/*
This file contains helper templates and values that can be used throughout the chart.
*/}}

{{/* Define a fullname template to generate the full name of resources */}}
{{- define "request-data.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name }}
{{- end }}

{{/* Define a name template to generate a generic name for resources */}}
{{- define "request-data.name" -}}
{{- printf "%s" .Chart.Name }}
{{- end }}
