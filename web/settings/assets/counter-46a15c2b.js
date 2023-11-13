import{_ as g,p as d,k as p,l as _,A as n,L as u,u as r,q as s,x as b}from"./vendor-94ac8c48.js";import"./vendor-sortablejs-dbc23470.js";const c={name:"DeviceJsonCounter",emits:["update:configuration"],props:{configuration:{type:Object,required:!0},deviceId:{default:void 0},componentId:{required:!0}},methods:{updateConfiguration(i,e=void 0){this.$emit("update:configuration",{value:i,object:e})}}},w={class:"device-json-counter"},v={class:"small"},j=s("br",null,null,-1);function q(i,e,o,h,x,a){const f=d("openwb-base-heading"),l=d("openwb-base-text-input"),m=d("openwb-base-alert");return p(),_("div",w,[n(f,null,{default:u(()=>[r(" Einstellungen für JSON Zähler "),s("span",v,"(Modul: "+b(i.$options.name)+")",1)]),_:1}),n(l,{title:"Abfrage für Leistung",subtype:"text",required:"","model-value":o.configuration.jq_power,"onUpdate:modelValue":e[0]||(e[0]=t=>a.updateConfiguration(t,"configuration.jq_power"))},{help:u(()=>[r(' Zur Analyse der Werte aus dem json-Objekt wird jq benutzt. Ist die Json Antwort z.B. {"PowerInstalledPeak":4655, "PowerProduced":132, "PowerOut":897.08172362555717, "PowerSelfSupplied":234.9182763744428} So muss hier .PowerOut eingetragen werden. '),j,r(" Es wird vom Server eine Zahl mit oder ohne Nachkommastellen (Float, Integer) und einem Punkt als Dezimaltrennzeichen erwartet, welche die aktuelle Leistung in Watt darstellt. ")]),_:1},8,["model-value"]),n(l,{title:"Abfrage für Zählerstand Bezug",subtype:"text","model-value":o.configuration.jq_imported,"onUpdate:modelValue":e[1]||(e[1]=t=>a.updateConfiguration(t,"configuration.jq_imported"))},{help:u(()=>[r(" Wird dieses Feld leer gelassen, dann werden Zählerstände intern simuliert. ")]),_:1},8,["model-value"]),n(l,{title:"Abfrage für Zählerstand Einspeisung",subtype:"text","model-value":o.configuration.jq_exported,"onUpdate:modelValue":e[2]||(e[2]=t=>a.updateConfiguration(t,"configuration.jq_exported"))},{help:u(()=>[r(" Wird dieses Feld leer gelassen, dann werden Zählerstände intern simuliert. ")]),_:1},8,["model-value"]),n(m,{subtype:"info"},{default:u(()=>[r(" Werden sowohl Leistung als auch Strom auf den Einzelphasen leer gelassen, erfolgt das Lastmanagement am EVU-Punkt nur anhand der Gesamtleistung am EVU-Punkt. Wird der Zähler als Zwischenzähler verwendet, wird in diesem Fall kein Lastmanagement durchgeführt. ")]),_:1}),n(l,{title:"Abfrage für Leistung auf Phase 1",subtype:"text","model-value":o.configuration.jq_power_l1,"onUpdate:modelValue":e[3]||(e[3]=t=>a.updateConfiguration(t,"configuration.jq_power_l1"))},null,8,["model-value"]),n(l,{title:"Abfrage für Leistung auf Phase 2",subtype:"text","model-value":o.configuration.jq_power_l2,"onUpdate:modelValue":e[4]||(e[4]=t=>a.updateConfiguration(t,"configuration.jq_power_l2"))},null,8,["model-value"]),n(l,{title:"Abfrage für Leistung auf Phase 3",subtype:"text","model-value":o.configuration.jq_power_l3,"onUpdate:modelValue":e[5]||(e[5]=t=>a.updateConfiguration(t,"configuration.jq_power_l3"))},null,8,["model-value"]),n(l,{title:"Abfrage für Strom auf Phase 1",subtype:"text","model-value":o.configuration.jq_current_l1,"onUpdate:modelValue":e[6]||(e[6]=t=>a.updateConfiguration(t,"configuration.jq_current_l1"))},null,8,["model-value"]),n(l,{title:"Abfrage für Strom auf Phase 2",subtype:"text","model-value":o.configuration.jq_current_l2,"onUpdate:modelValue":e[7]||(e[7]=t=>a.updateConfiguration(t,"configuration.jq_current_l2"))},null,8,["model-value"]),n(l,{title:"Abfrage für Strom auf Phase 3",subtype:"text","model-value":o.configuration.jq_current_l3,"onUpdate:modelValue":e[8]||(e[8]=t=>a.updateConfiguration(t,"configuration.jq_current_l3"))},null,8,["model-value"])])}const y=g(c,[["render",q],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/json/counter.vue"]]);export{y as default};