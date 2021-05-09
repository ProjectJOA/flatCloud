import main.flatcloud_main as flatcloud
import json

def go_main():
    flatcloud.start_main()

def go_second_menu(selected_first_menu):
    print("이전 메뉴로 이동합니다.")
    flatcloud.go_first_menu(selected_first_menu)
