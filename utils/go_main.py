import main.flatcloud_main as flatcloud
import json

def go_main():
    flatcloud.start_main()

def go_secondOrExit(inputVal, selected_first_menu):
    try:
        if inputVal.lower() == "p":
            go_second_menu(selected_first_menu)
        elif inputVal.lower() == "x":
            exit_flatcloud()
    except Exception as e:
        print("move page exception occured!!",e)
    return "success"

def go_second_menu(selected_first_menu):
    print("이전 메뉴로 이동합니다.")
    flatcloud.go_first_menu(selected_first_menu)

def exit_flatcloud():
    print("flatCloud를 종료합니다.")
    exit()