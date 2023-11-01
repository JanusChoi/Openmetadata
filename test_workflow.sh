# 请注意修改以下代码为你本机路径
# 此脚本仅为便于测试使用
cd /yourpath/code/alfred-workflow

query=$1
OLD_IFS="$IFS"
IFS=","

argvs=($query)
echo "参数调试:"${argvs} > /yourpath/code/alfred-workflow/run.log
/yourpath/opt/anaconda3/envs/311/bin/python /yourpath/code/alfred-workflow/text_chat_main.py ${argvs} >> /yourpath/code/alfred-workflow/run.log

# count=0
# for argv in ${argvs[@]}; do
#     if [ ${count} -eq 0 ]; then
#         template=${argv}
#         echo "应用模板:"${template} >> /yourpath/code/alfred-workflow/run.log
#     fi
#     if [ ${count} -eq 1 ]; then
#         context=${argv}
#         echo ${context} > /yourpath/code/alfred-workflow/tmp_context.tmp
#         echo "上下文记录完成" >> /yourpath/code/alfred-workflow/run.log
#         /yourpath/opt/anaconda3/envs/311/bin/python /yourpath/code/alfred-workflow/text_chat_main.py ${template} >> /yourpath/code/alfred-workflow/run.log
#         echo "py执行完毕" >> /yourpath/code/alfred-workflow/run.log
#     fi
#     let count=count+1
# done