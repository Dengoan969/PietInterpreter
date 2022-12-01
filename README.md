# Piet Interpreter
---
## Version 1.0

## Описание
Данный интерпретатор даёт возможность для выполнения и отладки программ на языке Piet
## Инструкция по запуску
Запуск осуществляется в консольном режиме.   

Команда запуска имеет вид: `piet.py [--debug] PATH`  

Параметры:  
--debug -- флаг для выполнения программы в режиме отладки  
PATH -- путь к файлу программы в формате PNG, JPG, BMP или GIF
## Подробности реализации
Перед началом выполнения, интерпретатор находит все цветные блоки, определяет  
их границы, команды, которые будут выполнены на границах при переходе.   

Далее,в зависимости от Direction Pointer (DP) и Codel Chooser (CC)  
выбирается команда для выполнения. Изменения после выполнения команды  
возвращаются как новое состояние выполнения программы(State)