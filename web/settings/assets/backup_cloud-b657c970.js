import{_ as m,p as r,k as b,l as _,A as o,L as d,u as l,q as i,x as c}from"./vendor-94ac8c48.js";import"./vendor-sortablejs-dbc23470.js";const f={name:"BackupCloudSamba",emits:["update:configuration"],props:{configuration:{type:Object,required:!0}},data(){return{}},methods:{updateConfiguration(s,e=void 0){this.$emit("update:configuration",{value:s,object:e})}}},g={class:"backup-cloud-samba"},v={class:"small"},w=i("br",null,null,-1),C=i("br",null,null,-1),k=i("br",null,null,-1);function B(s,e,t,h,V,a){const p=r("openwb-base-heading"),u=r("openwb-base-text-input");return b(),_("div",g,[o(p,null,{default:d(()=>[l(" Einstellungen für Samba-Backup Cloud "),i("span",v,"(Modul: "+c(s.$options.name)+")",1)]),_:1}),o(u,{title:"Server",subtype:"host",required:"","model-value":t.configuration.smb_server,"onUpdate:modelValue":e[0]||(e[0]=n=>a.updateConfiguration(n,"configuration.smb_server"))},null,8,["model-value"]),o(u,{title:"Freigabe",required:"","model-value":t.configuration.smb_share,"onUpdate:modelValue":e[1]||(e[1]=n=>a.updateConfiguration(n,"configuration.smb_share"))},null,8,["model-value"]),o(u,{title:"Unterordner (optional)","model-value":t.configuration.smb_path,pattern:'([^\\\\:"\\|*?<>]+/)*',"onUpdate:modelValue":e[2]||(e[2]=n=>a.updateConfiguration(n,"configuration.smb_path"))},{help:d(()=>[l(" Jeder Unterordner muss mit / enden."),w,l(' Die Zeichen \\:"|*?<> sind verboten!'),C,l(" Beispiel 1: openwb/ "),k,l(" Beispiel 2: openwb/lp2/ ")]),_:1},8,["model-value"]),o(u,{title:"Benutzer",subtype:"user","model-value":t.configuration.smb_user,"onUpdate:modelValue":e[3]||(e[3]=n=>a.updateConfiguration(n,"configuration.smb_user"))},null,8,["model-value"]),o(u,{title:"Kennwort",subtype:"password","model-value":t.configuration.smb_password,"onUpdate:modelValue":e[4]||(e[4]=n=>a.updateConfiguration(n,"configuration.smb_password"))},null,8,["model-value"])])}const y=m(f,[["render",B],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/backup_clouds/samba/backup_cloud.vue"]]);export{y as default};