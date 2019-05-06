# Offline audio package

## Usage
`roslaunch voice_bringup_offline voice_bringup_offline.launch`

Replace online **iflytek_asr** and **tuling_nlu** with **offline_asr** and **offline_nlp** respectively. The api has been matched corrected. Further improvement on model can be extended.

## Offline asr
Use CMUsphinx for audio speech recognition

1. Install dependency packages
    * For Ubuntu: sudo apt-get install -qq python python-dev python-pip build-essential swig git libpulse-dev libasound2-dev
2. Install [Pocketsphinx Python](https://github.com/bambocher/pocketsphinx-python)
    * python -m pip install --upgrade pip setuptools wheel
    * pip install --upgrade pocketsphinx
3. Expand the command set (Optional)
    * List command words like `command.txt`
    * Upload the document to [Sphinx KB Tool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html)
    * Download `****.lm`, e.g. `6159.lm`. Rename as `zh_command.lm` and move to `./model/`
    * Update `./model/zh_command.dic`, consistent with `./model/zh_command.lm`. The required pinyin can be searched in `./model/zh_cn.dic`

## Offline nlp
Simply match the input text with pre-defined commands

## Tips
1. py文件在launch中需要在name加入.py，并注意chmod权限
2. catkin_make在当前目录编译，并source ~/catkin_ws/devel/setup.bash
3. ros中代码的路径名避免用相对路径