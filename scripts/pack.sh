#!/bin/bash  

pyinstaller MinecraftMotd.spec

mkdir -p bin
cp -r dist/* bin/

mkdir -p bin/lang
cp -r lang/* bin/lang/

rm -rf dist
rm -rf build