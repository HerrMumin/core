import{_ as u,u as n,k as l,l as d,D as r,N as s,y as t,x as a,z as p}from"./vendor-f2b8aa6f.js";import"./vendor-sortablejs-2f1828d0.js";const _={name:"DeviceKostalPlenticoreCounter",emits:["update:configuration"],props:{configuration:{type:Object,required:!0},deviceId:{default:void 0},componentId:{required:!0}},methods:{updateConfiguration(e,o=void 0){this.$emit("update:configuration",{value:e,object:o})}}},f={class:"device-kostalplenticore-counter"},h={class:"small"},m=a("a",{href:"https://github.com/openWB/core/wiki/Hausverbrauchs-Zähler",target:"_blank",rel:"noopener noreferrer"},"Wiki für Hausverbrauchs-Zähler",-1);function b(e,o,g,v,w,k){const i=n("openwb-base-heading"),c=n("openwb-base-alert");return l(),d("div",f,[r(i,null,{default:s(()=>[t(" Einstellungen für Kostal Plenticore Zähler "),a("span",h,"(Modul: "+p(e.$options.name)+")",1)]),_:1}),r(c,{subtype:"info"},{default:s(()=>[t(" Wenn der Zähler im Hausverbrauchs-Zweig installiert ist, muss die Hierarchie wie im "),m,t(" beschrieben, angeordnet werden. ")]),_:1})])}const B=u(_,[["render",b],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/kostal_plenticore/counter.vue"]]);export{B as default};