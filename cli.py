from data import *
from logic import *
from ascii_text import *
import inquirer
import os
import click

from inquirer.themes import GreenPassion


def welcome_cli():
    os.system('clear')
    print(title_pc_part_picker)
    print(title_welcome)
    click.echo(f'{YELLOW}Press any button to continue.', nl=False)
    c = click.getchar()
    click.echo()
    os.system('clear')
    main_menu_cli()

def main_menu_cli():
    print(f"{title_main_menu}\n")
    mm_questions = [
        inquirer.List(
        "main_menu_selector",
        message="Select",
        choices=["Create New Computer", "View Existing Computers"],
        )
    ]
    mm_answers = inquirer.prompt(mm_questions)
    if mm_answers['main_menu_selector'] == "Create New Computer":
        os.system('clear')
        create_computer_cli()
    elif mm_answers['main_menu_selector'] == "View Existing Computers":
        os.system('clear')
        view_computer_cli()

def create_computer_cli():
    print(f"{title_create_computer}\n")
    create_computer_questions = [
    inquirer.Text(name="new_pc_name", message="Type the name of the new computer or 'MAIN MENU' to return to the main menu")
    ]
    create_computer_answers = inquirer.prompt(create_computer_questions)
    upper_answer = create_computer_answers["new_pc_name"]
    if upper_answer.upper() == 'MAIN MENU':
        os.system('clear')
        main_menu_cli()
    elif create_computer_answers["new_pc_name"]:
        name_compare = find_computer_by_name(create_computer_answers["new_pc_name"])
        if name_compare is None:
            create_confirm_questions = [
                inquirer.Confirm('confirm_create', message=f'Name your computer {create_computer_answers["new_pc_name"]}?')
            ]
            create_confirm_answers = inquirer.prompt(create_confirm_questions)
            if create_confirm_answers['confirm_create']:
                create_computer(create_computer_answers["new_pc_name"])
                print(f'Created {create_computer_answers["new_pc_name"]}!')
                click.echo('Press any button to retrun to the main menu.')
                c = click.getchar()
                click.echo()
                os.system('clear')
                main_menu_cli()
            else:
                os.system('clear')
                create_computer_cli()
        else:
            print(f'A computer with the name {create_computer_answers["new_pc_name"]} already exists')
            click.echo('Press any button to continue.')
            c = click.getchar()
            click.echo()
            os.system('clear')
            create_computer_cli()
    else:
        print("Please enter a valid name")
        click.echo('Press any button to continue.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        create_computer_cli()


def view_computer_cli():
    print(f"{title_your_computers}\n")
    with Session(engine) as session:
        computers = session.query(Computer).all()
        computer_names = [computer.name for computer in computers]
        computer_names_mm = [computer.name for computer in computers]
        computer_names_mm.append(f"{YELLOW}RETURN TO MAIN MENU")
    view_computer_questions = [
        inquirer.List(
        "view_computer_selector",
        message="VIEW OPTIONS FOR",
        choices=computer_names_mm,
        )
    ]
    view_computer_answers = inquirer.prompt(view_computer_questions)
    if view_computer_answers["view_computer_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
        os.system('clear')
        main_menu_cli()
    else:
        cli_computer = find_computer_by_name(view_computer_answers["view_computer_selector"])
        os.system('clear')
        view_computer_options_cli(cli_computer)

def view_computer_options_cli(cli_computer):
    print(f"{title_options}\n")
    print(f"{cli_computer.name.upper()} OPTIONS")
    view_computer_options_questions = [
        inquirer.List(
        "view_options",
        message=f'What would you like to do with {cli_computer.name}',
        choices=["View Parts", "Add Part", f"{YELLOW}RETURN TO YOUR COMPUTERS", f"{RED}DELETE {cli_computer.name.upper()}"],
        )
    ]
    view_computer_options_answers = inquirer.prompt(view_computer_options_questions)
    if view_computer_options_answers["view_options"] == "View Parts":
        os.system('clear')
        view_computer_details_cli(cli_computer)
    elif view_computer_options_answers["view_options"] == "Add Part":
        os.system('clear')
        add_part_option_cli(cli_computer)
    elif view_computer_options_answers["view_options"] == f"{YELLOW}RETURN TO YOUR COMPUTERS":
        os.system('clear')
        view_computer_cli()
    elif view_computer_options_answers["view_options"] == f"{RED}DELETE {cli_computer.name.upper()}":
        delete_computer_cli(cli_computer)
    else:
        os.system('clear')
        print("NOT A VALID OPTION")
        view_computer_cli()

def delete_computer_cli(cli_computer):
    delete_computer_questions = [
    inquirer.Confirm(name="delete_computer", message=f"{RED}Are you sure you want to delete {cli_computer.name}")
    ]
    delete_computer_answers = inquirer.prompt(delete_computer_questions)
    if delete_computer_answers["delete_computer"]:
        remove_computer(cli_computer.id)
        click.echo('Press any button to continue.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        view_computer_cli()

def view_computer_details_cli(cli_computer):
    print(f"{title_view_parts}\n")
    print(f'VIEWING {cli_computer.name.upper()} PARTS')
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=cli_computer.id).first()
        c_computer_parts = [
            c_computer.cpu,
            c_computer.gpu,
            c_computer.motherboard,
            c_computer.ram,
            c_computer.storage,
            c_computer.cpu_cooler,
            c_computer.power_supply,
            c_computer.case
        ]
        c_computer_part_names = []
        for part in c_computer_parts:
            if part is None:
                c_computer_part_names.append(None)
            else:
                c_computer_part_names.append(part.name)
        c_computer_part_options = c_computer_part_names
        c_computer_part_options.extend([f"{YELLOW}RETRUN TO {cli_computer.name.upper()} OPTIONS", f"{RED}REMOVE A PART?"])
        view_computer_details_questions = [
            inquirer.List(
            "part_selector",
            message="SELECT A PART TO VIEW THE DETAILS OF THAT PART",
            choices=[
                f"0: CPU: {c_computer_part_options[0]}",
                f"1: GPU: {c_computer_part_options[1]}",
                f"2: Motherboard: {c_computer_part_options[2]}",
                f"3: RAM: {c_computer_part_options[3]}",
                f"4: Storage: {c_computer_part_options[4]}",
                f"5: CPU Cooler: {c_computer_part_options[5]}",
                f"6: Power Supply: {c_computer_part_options[6]}",
                f"7: Case: {c_computer_part_options[7]}",
                c_computer_part_options[8],
                c_computer_part_options[9],
            ],
            )
        ]
        view_computer_details_answers = inquirer.prompt(view_computer_details_questions)
        if view_computer_details_answers["part_selector"].endswith("OPTIONS"):
            os.system('clear')
            view_computer_options_cli(cli_computer)
        elif view_computer_details_answers["part_selector"].endswith("PART?"):
            os.system('clear')
            remove_part_cli(cli_computer, c_computer_part_names)
        else:
            selected_part_index = int(view_computer_details_answers["part_selector"].split(": ")[0])
            selected_part_type = str(view_computer_details_answers["part_selector"].split(": ")[1])
            if c_computer_parts[selected_part_index] is None:
                part_details = f"There is no {selected_part_type} in {cli_computer.name}."
                none_part_questions = [
                inquirer.Confirm(name="none_part", message=f"There is no {selected_part_type} in {cli_computer.name}. Would you like to add one?")
                ]
                none_part_answers = inquirer.prompt(none_part_questions)
                if none_part_answers["none_part"]:
                    if selected_part_index is 0:
                        os.system('clear')
                        add_part_cpu_cli(cli_computer)
                    elif selected_part_index is 1:
                        os.system('clear')
                        add_part_gpu_cli(cli_computer)
                    elif selected_part_index is 2:
                        os.system('clear')
                        add_part_motherboard_cli(cli_computer)
                    elif selected_part_index is 3:
                        os.system('clear')
                        add_part_ram_cli(cli_computer)
                    elif selected_part_index is 4:
                        os.system('clear')
                        add_part_storage_cli(cli_computer)
                    elif selected_part_index is 5:
                        os.system('clear')
                        add_part_cpu_cooler_cli(cli_computer)
                    elif selected_part_index is 6:
                        os.system('clear')
                        add_part_power_supply_cli(cli_computer)
                    elif selected_part_index is 7:
                        os.system('clear')
                        add_part_case_cli(cli_computer)             
            else:
                selected_part = c_computer_parts[selected_part_index]
                part_details = selected_part.display_details()
                os.system('clear')
                print("DETAILS:")
                for part_type, part in part_details.items():
                    print(f"{part_type}: {part}")
                view_computer_details_cli(cli_computer)

def remove_part_cli(cli_computer, c_computer_part_names):
    c_computer_part_options = c_computer_part_names
    c_computer_part_options.append([f"{YELLOW}RETRUN TO {cli_computer.name.upper()} OPTIONS"])
    while True:
        view_computer_details_questions = [
            inquirer.List(
            "part_delete_selector",
            message="SELECT THE PART YOU WOULD LIKE TO REMOVE",
            choices=[
                f"{RED}DELETE: 0: CPU: {c_computer_part_options[0]}",
                f"{RED}DELETE: 1: GPU: {c_computer_part_options[1]}",
                f"{RED}DELETE: 2: Motherboard: {c_computer_part_options[2]}",
                f"{RED}DELETE: 3: RAM: {c_computer_part_options[3]}",
                f"{RED}DELETE: 4: Storage: {c_computer_part_options[4]}",
                f"{RED}DELETE: 5: CPU Cooler: {c_computer_part_options[5]}",
                f"{RED}DELETE: 6: Power Supply: {c_computer_part_options[6]}",
                f"{RED}DELETE: 7: Case: {c_computer_part_options[7]}",
                c_computer_part_options[8],
            ],
            )
        ]
        view_computer_details_answers = inquirer.prompt(view_computer_details_questions)
        if view_computer_details_answers["part_delete_selector"].endswith("OPTIONS"):
                os.system('clear')
                break
        else:
                selected_part_index = int(view_computer_details_answers["part_delete_selector"].split(": ")[1])
                selected_part_type = str(view_computer_details_answers["part_delete_selector"].split(": ")[2])
                if c_computer_part_names[selected_part_index] == None:
                    os.system('clear')
                    print(f"{CYAN}{cli_computer.name} doesn't contain a {selected_part_type}")
                    continue
                else:
                    remove_part_questions = [
                    inquirer.Confirm(name="remove_part_confirm", message=f"Are you sure you want to remove {c_computer_part_names[selected_part_index]} from {cli_computer.name}?")
                    ]
                    remove_part_answers = inquirer.prompt(remove_part_questions)
                    if remove_part_answers["remove_part_confirm"]:
                        if selected_part_index is 0:
                            remove_from_computer(cli_computer.id, "cpu")
                            click.echo(f'{c_computer_part_names[selected_part_index]} removed! Press any button to retrun to {cli_computer.name} options.')
                            c = click.getchar()
                            click.echo()
                            break
                        elif selected_part_index is 1:
                            remove_from_computer(cli_computer.id, "gpu")
                            click.echo(f'{c_computer_part_names[selected_part_index]} removed! Press any button to retrun to {cli_computer.name} options.')
                            c = click.getchar()
                            click.echo()
                            break
                        elif selected_part_index is 2:
                            remove_from_computer(cli_computer.id, "motherboard")
                            click.echo(f'{c_computer_part_names[selected_part_index]} removed! Press any button to retrun to {cli_computer.name} options.')
                            c = click.getchar()
                            click.echo()
                            break
                        elif selected_part_index is 3:
                            remove_from_computer(cli_computer.id, "ram")
                            click.echo(f'{c_computer_part_names[selected_part_index]} removed! Press any button to retrun to {cli_computer.name} options.')
                            c = click.getchar()
                            click.echo()
                            break
                        elif selected_part_index is 4:
                            remove_from_computer(cli_computer.id, "storage")
                            click.echo(f'{c_computer_part_names[selected_part_index]} removed! Press any button to retrun to {cli_computer.name} options.')
                            c = click.getchar()
                            click.echo()
                            break
                        elif selected_part_index is 5:
                            remove_from_computer(cli_computer.id, "cpu_cooler")
                            click.echo(f'{c_computer_part_names[selected_part_index]} removed! Press any button to retrun to {cli_computer.name} options.')
                            c = click.getchar()
                            click.echo()
                            break
                        elif selected_part_index is 6:
                            remove_from_computer(cli_computer.id, "power_supply")
                            click.echo(f'{c_computer_part_names[selected_part_index]} removed! Press any button to retrun to {cli_computer.name} options.')
                            c = click.getchar()
                            click.echo()
                            break
                        elif selected_part_index is 7:
                            remove_from_computer(cli_computer.id, "case")
                            click.echo(f'{c_computer_part_names[selected_part_index]} removed! Press any button to retrun to {cli_computer.name} options.')
                            c = click.getchar()
                            click.echo()
                            break
                    else:
                        os.system('clear')
                        continue
    os.system('clear')
    view_computer_options_cli(cli_computer)



def add_part_option_cli(cli_computer):
    print(f"{title_add_parts_menu}\n")
    print(f'ADDING PARTS TO: {cli_computer.name.upper()}')
    with Session(engine) as session:
        c_computer = session.query(Computer).filter_by(id=cli_computer.id).first()
        c_computer_parts = [
            c_computer.cpu,
            c_computer.gpu,
            c_computer.motherboard,
            c_computer.ram,
            c_computer.storage,
            c_computer.cpu_cooler,
            c_computer.power_supply,
            c_computer.case
        ]
        c_computer_part_names = []
        for part in c_computer_parts:
            if part is None:
                c_computer_part_names.append(None)
            else:
                c_computer_part_names.append(part.name)
        c_computer_contains = [
                f"CPU: {c_computer_part_names[0]}",
                f"GPU: {c_computer_part_names[1]}",
                f"Motherboard: {c_computer_part_names[2]}",
                f"RAM: {c_computer_part_names[3]}",
                f"Storage: {c_computer_part_names[4]}",
                f"CPU Cooler: {c_computer_part_names[5]}",
                f"Power Supply: {c_computer_part_names[6]}",
                f"Case: {c_computer_part_names[7]}",
            ],
        
        add_part_option_qusetion = [
                inquirer.List(
                "part_add_selector",
                message="SELECT TYPE OF PART YOU WOULD LIKE TO ADD OR WHERE YOU WOULD LIKE TO NAVIGATE",
                choices=[
                    "CPU",
                    "GPU",
                    "Motherboard",
                    "RAM",
                    "Storage",
                    "CPU Cooler",
                    "Power Supply",
                    "Case",
                    f"{YELLOW}RETURN TO MAIN MENU",
                    f"{YELLOW}RETURN TO {cli_computer.name} OPTIONS"
                ],
                )
            ]
        add_part_option_answer = inquirer.prompt(add_part_option_qusetion)
        if add_part_option_answer["part_add_selector"] == "CPU":
            os.system('clear')
            add_part_cpu_cli(cli_computer)
        elif add_part_option_answer["part_add_selector"] == "GPU":
            os.system('clear')
            add_part_gpu_cli(cli_computer)
        elif add_part_option_answer["part_add_selector"] == "Motherboard":
            os.system('clear')
            add_part_motherboard_cli(cli_computer)
        elif add_part_option_answer["part_add_selector"] == "RAM":
            os.system('clear')
            add_part_ram_cli(cli_computer)
        elif add_part_option_answer["part_add_selector"] == "Storage":
            os.system('clear')
            add_part_storage_cli(cli_computer)
        elif add_part_option_answer["part_add_selector"] == "CPU Cooler":
            os.system('clear')
            add_part_cpu_cooler_cli(cli_computer)
        elif add_part_option_answer["part_add_selector"] == "Power Supply":
            os.system('clear')
            add_part_power_supply_cli(cli_computer)
        elif add_part_option_answer["part_add_selector"] == "Case":
            os.system('clear')
            add_part_case_cli(cli_computer)
        elif add_part_option_answer["part_add_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
            os.system('clear')
            main_menu_cli()
        elif add_part_option_answer["part_add_selector"] == f"{YELLOW}RETURN TO {cli_computer.name} OPTIONS":
            os.system('clear')
            view_computer_options_cli(cli_computer)

#CPU//////////////////////////////////////////////////////////////////////////////
def add_part_cpu_cli(cli_computer, list=[]):
    print(f"{tile_add_cpu}")
    if len(list) is 0:
        valid_cpu_names = [cpu.name for cpu in valid_cpu(cli_computer.id)]
    else:
        valid_cpu_names = list
    add_valid_cpu_options = [
        # f"{GREEN}FILTER",
        f"{CYAN}SORT",
        f"{YELLOW}RETURN TO MAIN MENU",
        f"{YELLOW}RETURN TO ADD PART MENU"
    ]
    add_valid_cpu_options.extend(valid_cpu_names)
    # print(valid_cpu_names)
    # print(add_valid_cpu_options)

    add_valid_cpu_qusetion = [
            inquirer.List(
            "add_cpu_selector",
            message="SELECT PART YOU WOULD LIKE TO SEE DETAILS OF OR WHERE YOU WOULD LIKE TO NAVIGATE",
            choices=add_valid_cpu_options
            )
        ]
    add_valid_cpu_answer = inquirer.prompt(add_valid_cpu_qusetion)
    if add_valid_cpu_answer["add_cpu_selector"] == f"{GREEN}FILTER":
        os.system('clear')
        print("FILTER MENU")
    elif add_valid_cpu_answer["add_cpu_selector"] == f"{CYAN}SORT":
        os.system('clear')
        print("SORT MENU")
        handle_motherboard_sort(cli_computer, valid_cpu_names)
    elif add_valid_cpu_answer["add_cpu_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
        os.system('clear')
        main_menu_cli()
    elif add_valid_cpu_answer["add_cpu_selector"] == f"{YELLOW}RETURN TO ADD PART MENU":
        os.system('clear')
        add_part_option_cli(cli_computer)
    else:
        part_name = add_valid_cpu_answer["add_cpu_selector"]
        handle_add_cpu_cli(cli_computer, part_name)

def handle_add_cpu_cli(cli_computer, part_name):
    cpu = find_part_by_name("cpu", part_name)
    part_details = cpu.display_details()
    print("DETAILS:")
    for part_type, part in part_details.items():
        print(f"{part_type}: {part}")
    handle_add_cpu_questions = [
                inquirer.Confirm('confirm_add_cpu', message=f'Add {cpu.name} to {cli_computer.name}?')
            ]
    handle_add_cpu_answers = inquirer.prompt(handle_add_cpu_questions)
    if handle_add_cpu_answers['confirm_add_cpu']:
        # print(f"{cli_computer.id}, 'cpu', {cpu.id}")
        add_to_computer(cli_computer.id, "cpu", cpu.id)
        print(f'{cpu.name} has been added to {cli_computer.name}!')
        click.echo(f'Press any button to retrun to {cli_computer.name} options.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        view_computer_options_cli(cli_computer)
    else:
        os.system('clear')
        add_part_cpu_cli(cli_computer)

def handle_cpu_sort(cli_computer, list):
    handle_cpu_sort_qusetion = [
            inquirer.List(
            "cpu_sort",
            message="FILTER BY:",
            choices=[
                "Alphabetical Ascending",
                "Alphabetical Descending",
                f"{YELLOW}BACK TO RESULTS"
            ]
            )
        ]
    handle_cpu_sort_answers = inquirer.prompt(handle_cpu_sort_qusetion)
    if handle_cpu_sort_answers["cpu_sort"] == "Alphabetical Ascending":
        sorted_list = sorted(list)
        os.system('clear')
        add_part_cpu_cli(cli_computer, sorted_list)
    elif handle_cpu_sort_answers["cpu_sort"] == "Alphabetical Descending":
        sorted_list = sorted(list, reverse=True)
        os.system('clear')
        add_part_cpu_cli(cli_computer, sorted_list)
    elif handle_cpu_sort_answers["cpu_sort"] == f"{YELLOW}BACK TO RESULTS":
        os.system('clear')
        add_part_cpu_cli(cli_computer, list)
    else:
        os.system('clear')
        add_part_cpu_cli(cli_computer, list)



#GPU //////////////////////////////////////////////////////////////////////////
def add_part_gpu_cli(cli_computer, list =[]):
    print(f"{title_add_gpu}")
    if len(list) is 0:
        valid_gpu_names = [gpu.name for gpu in valid_gpu(cli_computer.id)]
    else:
        valid_gpu_names = list
    add_valid_gpu_options = [
        # f"{GREEN}FILTER",
        f"{CYAN}SORT",
        f"{YELLOW}RETURN TO MAIN MENU",
        f"{YELLOW}RETURN TO ADD PART MENU"
    ]
    add_valid_gpu_options.extend(valid_gpu_names)
    # print(valid_gpu_names)
    # print(add_valid_gpu_options)

    add_valid_gpu_qusetion = [
            inquirer.List(
            "add_gpu_selector",
            message="SELECT PART YOU WOULD LIKE TO SEE DETAILS OF OR WHERE YOU WOULD LIKE TO NAVIGATE",
            choices=add_valid_gpu_options
            )
        ]
    add_valid_gpu_answer = inquirer.prompt(add_valid_gpu_qusetion)
    if add_valid_gpu_answer["add_gpu_selector"] == f"{GREEN}FILTER":
        os.system('clear')
        print("FILTER MENU")
    elif add_valid_gpu_answer["add_gpu_selector"] == f"{CYAN}SORT":
        os.system('clear')
        print("SORT MENU")
        handle_motherboard_sort(cli_computer, valid_gpu_names)
    elif add_valid_gpu_answer["add_gpu_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
        os.system('clear')
        main_menu_cli()
    elif add_valid_gpu_answer["add_gpu_selector"] == f"{YELLOW}RETURN TO ADD PART MENU":
        os.system('clear')
        add_part_option_cli(cli_computer)
    else:
        part_name = add_valid_gpu_answer["add_gpu_selector"]
        handle_add_gpu_cli(cli_computer, part_name)

def handle_add_gpu_cli(cli_computer, part_name):
    gpu = find_part_by_name("gpu", part_name)
    part_details = gpu.display_details()
    print("DETAILS:")
    for part_type, part in part_details.items():
        print(f"{part_type}: {part}")
    handle_add_gpu_questions = [
                inquirer.Confirm('confirm_add_gpu', message=f'Add {gpu.name} to {cli_computer.name}?')
            ]
    handle_add_gpu_answers = inquirer.prompt(handle_add_gpu_questions)
    if handle_add_gpu_answers['confirm_add_gpu']:
        # print(f"{cli_computer.id}, 'gpu', {gpu.id}")
        add_to_computer(cli_computer.id, "gpu", gpu.id)
        print(f'{gpu.name} has been added to {cli_computer.name}!')
        click.echo(f'Press any button to retrun to {cli_computer.name} options.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        view_computer_options_cli(cli_computer)
    else:
        os.system('clear')
        add_part_gpu_cli(cli_computer)

def handle_gpu_sort(cli_computer, list):
    handle_gpu_sort_qusetion = [
            inquirer.List(
            "gpu_sort",
            message="FILTER BY:",
            choices=[
                "Alphabetical Ascending",
                "Alphabetical Descending",
                f"{YELLOW}BACK TO RESULTS"
            ]
            )
        ]
    handle_gpu_sort_answers = inquirer.prompt(handle_gpu_sort_qusetion)
    if handle_gpu_sort_answers["gpu_sort"] == "Alphabetical Ascending":
        sorted_list = sorted(list)
        os.system('clear')
        add_part_gpu_cli(cli_computer, sorted_list)
    elif handle_gpu_sort_answers["gpu_sort"] == "Alphabetical Descending":
        sorted_list = sorted(list, reverse=True)
        os.system('clear')
        add_part_gpu_cli(cli_computer, sorted_list)
    elif handle_gpu_sort_answers["gpu_sort"] == f"{YELLOW}BACK TO RESULTS":
        os.system('clear')
        add_part_gpu_cli(cli_computer, list)
    else:
        os.system('clear')
        add_part_gpu_cli(cli_computer, list)


# MOTHERBOARD///////////////////////////////////////////////////////
def add_part_motherboard_cli(cli_computer, list=[]):
    print(f"{title_add_motherboard}")
    if len(list) is 0:
        valid_motherboard_names = [motherboard.name for motherboard in valid_motherboard(cli_computer.id)]
    else:
        valid_motherboard_names = list
    add_valid_motherboard_options = [
        # f"{GREEN}FILTER",
        f"{CYAN}SORT",
        f"{YELLOW}RETURN TO MAIN MENU",
        f"{YELLOW}RETURN TO ADD PART MENU"
    ]
    add_valid_motherboard_options.extend(valid_motherboard_names)
    # print(valid_motherboard_names)
    # print(add_valid_motherboard_options)

    add_valid_motherboard_qusetion = [
            inquirer.List(
            "add_motherboard_selector",
            message="SELECT PART YOU WOULD LIKE TO SEE DETAILS OF OR WHERE YOU WOULD LIKE TO NAVIGATE",
            choices=add_valid_motherboard_options
            )
        ]
    add_valid_motherboard_answer = inquirer.prompt(add_valid_motherboard_qusetion)
    if add_valid_motherboard_answer["add_motherboard_selector"] == f"{GREEN}FILTER":
        os.system('clear')
        print("FILTER MENU")
    elif add_valid_motherboard_answer["add_motherboard_selector"] == f"{CYAN}SORT":
        os.system('clear')
        print("SORT MENU")
        handle_motherboard_sort(cli_computer, valid_motherboard_names)
    elif add_valid_motherboard_answer["add_motherboard_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
        os.system('clear')
        main_menu_cli()
    elif add_valid_motherboard_answer["add_motherboard_selector"] == f"{YELLOW}RETURN TO ADD PART MENU":
        os.system('clear')
        add_part_option_cli(cli_computer)
    else:
        part_name = add_valid_motherboard_answer["add_motherboard_selector"]
        handle_add_motherboard_cli(cli_computer, part_name)

def handle_add_motherboard_cli(cli_computer, part_name):
    motherboard = find_part_by_name("motherboard", part_name)
    part_details = motherboard.display_details()
    print("DETAILS:")
    for part_type, part in part_details.items():
        print(f"{part_type}: {part}")
    handle_add_motherboard_questions = [
                inquirer.Confirm('confirm_add_motherboard', message=f'Add {motherboard.name} to {cli_computer.name}?')
            ]
    handle_add_motherboard_answers = inquirer.prompt(handle_add_motherboard_questions)
    if handle_add_motherboard_answers['confirm_add_motherboard']:
        # print(f"{cli_computer.id}, 'motherboard', {motherboard.id}")
        add_to_computer(cli_computer.id, "motherboard", motherboard.id)
        print(f'{motherboard.name} has been added to {cli_computer.name}!')
        click.echo(f'Press any button to retrun to {cli_computer.name} options.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        view_computer_options_cli(cli_computer)
    else:
        os.system('clear')
        add_part_motherboard_cli(cli_computer)

def handle_motherboard_sort(cli_computer, list):
    handle_motherboard_sort_qusetion = [
            inquirer.List(
            "motherboard_sort",
            message="FILTER BY:",
            choices=[
                "Alphabetical Ascending",
                "Alphabetical Descending",
                f"{YELLOW}BACK TO RESULTS"
            ]
            )
        ]
    handle_motherboard_sort_answers = inquirer.prompt(handle_motherboard_sort_qusetion)
    if handle_motherboard_sort_answers["motherboard_sort"] == "Alphabetical Ascending":
        sorted_list = sorted(list)
        os.system('clear')
        add_part_motherboard_cli(cli_computer, sorted_list)
    elif handle_motherboard_sort_answers["motherboard_sort"] == "Alphabetical Descending":
        sorted_list = sorted(list, reverse=True)
        os.system('clear')
        add_part_motherboard_cli(cli_computer, sorted_list)
    elif handle_motherboard_sort_answers["motherboard_sort"] == f"{YELLOW}BACK TO RESULTS":
        os.system('clear')
        add_part_motherboard_cli(cli_computer, list)
    else:
        os.system('clear')
        add_part_motherboard_cli(cli_computer, list)

# RAM ///////////////////////////////////////////////////////////////////
def add_part_ram_cli(cli_computer, list=[]):
    print(f"{title_add_ram}")
    if len(list) is 0:
        valid_ram_names = [ram.name for ram in valid_ram(cli_computer.id)]
    else:
        valid_ram_names = list
    add_valid_ram_options = [
        # f"{GREEN}FILTER",
        f"{CYAN}SORT",
        f"{YELLOW}RETURN TO MAIN MENU",
        f"{YELLOW}RETURN TO ADD PART MENU"
    ]
    add_valid_ram_options.extend(valid_ram_names)
    # print(valid_ram_names)
    # print(add_valid_ram_options)

    add_valid_ram_qusetion = [
            inquirer.List(
            "add_ram_selector",
            message="SELECT PART YOU WOULD LIKE TO SEE DETAILS OF OR WHERE YOU WOULD LIKE TO NAVIGATE",
            choices=add_valid_ram_options
            )
        ]
    add_valid_ram_answer = inquirer.prompt(add_valid_ram_qusetion)
    if add_valid_ram_answer["add_ram_selector"] == f"{GREEN}FILTER":
        os.system('clear')
        print("FILTER MENU")
    elif add_valid_ram_answer["add_ram_selector"] == f"{CYAN}SORT":
        os.system('clear')
        print("SORT MENU")
        handle_ram_sort(cli_computer, valid_ram_names)
    elif add_valid_ram_answer["add_ram_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
        os.system('clear')
        main_menu_cli()
    elif add_valid_ram_answer["add_ram_selector"] == f"{YELLOW}RETURN TO ADD PART MENU":
        os.system('clear')
        add_part_option_cli(cli_computer)
    else:
        part_name = add_valid_ram_answer["add_ram_selector"]
        handle_add_ram_cli(cli_computer, part_name)

def handle_add_ram_cli(cli_computer, part_name):
    ram = find_part_by_name("ram", part_name)
    part_details = ram.display_details()
    print("DETAILS:")
    for part_type, part in part_details.items():
        print(f"{part_type}: {part}")
    handle_add_ram_questions = [
                inquirer.Confirm('confirm_add_ram', message=f'Add {ram.name} to {cli_computer.name}?')
            ]
    handle_add_ram_answers = inquirer.prompt(handle_add_ram_questions)
    if handle_add_ram_answers['confirm_add_ram']:
        # print(f"{cli_computer.id}, 'ram', {ram.id}")
        add_to_computer(cli_computer.id, "ram", ram.id)
        print(f'{ram.name} has been added to {cli_computer.name}!')
        click.echo(f'Press any button to retrun to {cli_computer.name} options.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        view_computer_options_cli(cli_computer)
    else:
        os.system('clear')
        add_part_ram_cli(cli_computer)

def handle_ram_sort(cli_computer, list):
    handle_ram_sort_qusetion = [
            inquirer.List(
            "ram_sort",
            message="FILTER BY:",
            choices=[
                "Alphabetical Ascending",
                "Alphabetical Descending",
                f"{YELLOW}BACK TO RESULTS"
            ]
            )
        ]
    handle_ram_sort_answers = inquirer.prompt(handle_ram_sort_qusetion)
    if handle_ram_sort_answers["ram_sort"] == "Alphabetical Ascending":
        sorted_list = sorted(list)
        os.system('clear')
        add_part_ram_cli(cli_computer, sorted_list)
    elif handle_ram_sort_answers["ram_sort"] == "Alphabetical Descending":
        sorted_list = sorted(list, reverse=True)
        os.system('clear')
        add_part_ram_cli(cli_computer, sorted_list)
    elif handle_ram_sort_answers["ram_sort"] == f"{YELLOW}BACK TO RESULTS":
        os.system('clear')
        add_part_ram_cli(cli_computer, list)
    else:
        os.system('clear')
        add_part_ram_cli(cli_computer, list)


# STORAGE ////////////////////////////////////////////////////
def add_part_storage_cli(cli_computer, list=[]):
    print(f"{title_add_storage}")
    if len(list) is 0:
        valid_storage_names = [storage.name for storage in valid_storage(cli_computer.id)]
    else:
        valid_storage_names = list
    add_valid_storage_options = [
        # f"{GREEN}FILTER",
        f"{CYAN}SORT",
        f"{YELLOW}RETURN TO MAIN MENU",
        f"{YELLOW}RETURN TO ADD PART MENU"
    ]
    add_valid_storage_options.extend(valid_storage_names)
    # print(valid_storage_names)
    # print(add_valid_storage_options)

    add_valid_storage_qusetion = [
            inquirer.List(
            "add_storage_selector",
            message="SELECT PART YOU WOULD LIKE TO SEE DETAILS OF OR WHERE YOU WOULD LIKE TO NAVIGATE",
            choices=add_valid_storage_options
            )
        ]
    add_valid_storage_answer = inquirer.prompt(add_valid_storage_qusetion)
    if add_valid_storage_answer["add_storage_selector"] == f"{GREEN}FILTER":
        os.system('clear')
        print("FILTER MENU")
    elif add_valid_storage_answer["add_storage_selector"] == f"{CYAN}SORT":
        os.system('clear')
        print("SORT MENU")
        handle_storage_sort(cli_computer, valid_storage_names)
    elif add_valid_storage_answer["add_storage_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
        os.system('clear')
        main_menu_cli()
    elif add_valid_storage_answer["add_storage_selector"] == f"{YELLOW}RETURN TO ADD PART MENU":
        os.system('clear')
        add_part_option_cli(cli_computer)
    else:
        part_name = add_valid_storage_answer["add_storage_selector"]
        handle_add_storage_cli(cli_computer, part_name)

def handle_add_storage_cli(cli_computer, part_name):
    storage = find_part_by_name("storage", part_name)
    part_details = storage.display_details()
    print("DETAILS:")
    for part_type, part in part_details.items():
        print(f"{part_type}: {part}")
    handle_add_storage_questions = [
                inquirer.Confirm('confirm_add_storage', message=f'Add {storage.name} to {cli_computer.name}?')
            ]
    handle_add_storage_answers = inquirer.prompt(handle_add_storage_questions)
    if handle_add_storage_answers['confirm_add_storage']:
        # print(f"{cli_computer.id}, 'storage', {storage.id}")
        add_to_computer(cli_computer.id, "storage", storage.id)
        print(f'{storage.name} has been added to {cli_computer.name}!')
        click.echo(f'Press any button to retrun to {cli_computer.name} options.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        view_computer_options_cli(cli_computer)
    else:
        os.system('clear')
        add_part_storage_cli(cli_computer)


def handle_storage_sort(cli_computer, list):
    handle_storage_sort_qusetion = [
            inquirer.List(
            "storage_sort",
            message="FILTER BY:",
            choices=[
                "Alphabetical Ascending",
                "Alphabetical Descending",
                f"{YELLOW}BACK TO RESULTS"
            ]
            )
        ]
    handle_storage_sort_answers = inquirer.prompt(handle_storage_sort_qusetion)
    if handle_storage_sort_answers["storage_sort"] == "Alphabetical Ascending":
        sorted_list = sorted(list)
        os.system('clear')
        add_part_storage_cli(cli_computer, sorted_list)
    elif handle_storage_sort_answers["storage_sort"] == "Alphabetical Descending":
        sorted_list = sorted(list, reverse=True)
        os.system('clear')
        add_part_storage_cli(cli_computer, sorted_list)
    elif handle_storage_sort_answers["storage_sort"] == f"{YELLOW}BACK TO RESULTS":
        os.system('clear')
        add_part_storage_cli(cli_computer, list)
    else:
        os.system('clear')
        add_part_storage_cli(cli_computer, list)


#CPU COOLER//////////////////////////////////////////
def add_part_cpu_cooler_cli(cli_computer, list=[]):
    print(f"{title_add_cpu_cooler}")
    if len(list) is 0:
        valid_cpu_cooler_names = [cpu_cooler.name for cpu_cooler in valid_cpu_cooler(cli_computer.id)]
    else:
        valid_cpu_cooler_names = list
    add_valid_cpu_cooler_options = [
        # f"{GREEN}FILTER",
        f"{CYAN}SORT",
        f"{YELLOW}RETURN TO MAIN MENU",
        f"{YELLOW}RETURN TO ADD PART MENU"
    ]
    add_valid_cpu_cooler_options.extend(valid_cpu_cooler_names)
    # print(valid_cpu_cooler_names)
    # print(add_valid_cpu_cooler_options)

    add_valid_cpu_cooler_qusetion = [
            inquirer.List(
            "add_cpu_cooler_selector",
            message="SELECT PART YOU WOULD LIKE TO SEE DETAILS OF OR WHERE YOU WOULD LIKE TO NAVIGATE",
            choices=add_valid_cpu_cooler_options
            )
        ]
    add_valid_cpu_cooler_answer = inquirer.prompt(add_valid_cpu_cooler_qusetion)
    if add_valid_cpu_cooler_answer["add_cpu_cooler_selector"] == f"{GREEN}FILTER":
        os.system('clear')
        print("FILTER MENU")
    elif add_valid_cpu_cooler_answer["add_cpu_cooler_selector"] == f"{CYAN}SORT":
        os.system('clear')
        print("SORT MENU")
        handle_cpu_cooler_sort(cli_computer, valid_cpu_cooler_names)
    elif add_valid_cpu_cooler_answer["add_cpu_cooler_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
        os.system('clear')
        main_menu_cli()
    elif add_valid_cpu_cooler_answer["add_cpu_cooler_selector"] == f"{YELLOW}RETURN TO ADD PART MENU":
        os.system('clear')
        add_part_option_cli(cli_computer)
    else:
        part_name = add_valid_cpu_cooler_answer["add_cpu_cooler_selector"]
        handle_add_cpu_cooler_cli(cli_computer, part_name)

def handle_add_cpu_cooler_cli(cli_computer, part_name):
    cpu_cooler = find_part_by_name("cpu_cooler", part_name)
    part_details = cpu_cooler.display_details()
    print("DETAILS:")
    for part_type, part in part_details.items():
        print(f"{part_type}: {part}")
    handle_add_cpu_cooler_questions = [
                inquirer.Confirm('confirm_add_cpu_cooler', message=f'Add {cpu_cooler.name} to {cli_computer.name}?')
            ]
    handle_add_cpu_cooler_answers = inquirer.prompt(handle_add_cpu_cooler_questions)
    if handle_add_cpu_cooler_answers['confirm_add_cpu_cooler']:
        # print(f"{cli_computer.id}, 'cpu_cooler', {cpu_cooler.id}")
        add_to_computer(cli_computer.id, "cpu_cooler", cpu_cooler.id)
        print(f'{cpu_cooler.name} has been added to {cli_computer.name}!')
        click.echo(f'Press any button to retrun to {cli_computer.name} options.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        view_computer_options_cli(cli_computer)
    else:
        os.system('clear')
        add_part_cpu_cooler_cli(cli_computer)

def handle_cpu_cooler_sort(cli_computer, list):
    handle_cpu_cooler_sort_qusetion = [
            inquirer.List(
            "cpu_cooler_sort",
            message="FILTER BY:",
            choices=[
                "Alphabetical Ascending",
                "Alphabetical Descending",
                f"{YELLOW}BACK TO RESULTS"
            ]
            )
        ]
    handle_cpu_cooler_sort_answers = inquirer.prompt(handle_cpu_cooler_sort_qusetion)
    if handle_cpu_cooler_sort_answers["cpu_cooler_sort"] == "Alphabetical Ascending":
        sorted_list = sorted(list)
        os.system('clear')
        add_part_cpu_cooler_cli(cli_computer, sorted_list)
    elif handle_cpu_cooler_sort_answers["cpu_cooler_sort"] == "Alphabetical Descending":
        sorted_list = sorted(list, reverse=True)
        os.system('clear')
        add_part_cpu_cooler_cli(cli_computer, sorted_list)
    elif handle_cpu_cooler_sort_answers["cpu_cooler_sort"] == f"{YELLOW}BACK TO RESULTS":
        os.system('clear')
        add_part_cpu_cooler_cli(cli_computer, list)
    else:
        os.system('clear')
        add_part_cpu_cooler_cli(cli_computer, list)


#POWER SUPPLY ADD/////////////////////////////////////////////////////////////////////////////////////
def add_part_power_supply_cli(cli_computer, list=[]):
    print(f"{title_add_power_supply}")
    if len(list) is 0:
        valid_power_supply_names = [power_supply.name for power_supply in valid_power_supply(cli_computer.id)]
    else:
        valid_power_supply_names = list
    add_valid_power_supply_options = [
        # f"{GREEN}FILTER",
        f"{CYAN}SORT",
        f"{YELLOW}RETURN TO MAIN MENU",
        f"{YELLOW}RETURN TO ADD PART MENU"
    ]
    valid_power_supply_names
    add_valid_power_supply_options.extend(valid_power_supply_names)
    # print(valid_power_supply_names)
    # print(add_valid_power_supply_options)

    add_valid_power_supply_qusetion = [
            inquirer.List(
            "add_power_supply_selector",
            message="SELECT PART YOU WOULD LIKE TO SEE DETAILS OF OR WHERE YOU WOULD LIKE TO NAVIGATE",
            choices=add_valid_power_supply_options
            )
        ]
    add_valid_power_supply_answer = inquirer.prompt(add_valid_power_supply_qusetion)
    if add_valid_power_supply_answer["add_power_supply_selector"] == f"{GREEN}FILTER":
        os.system('clear')
        print("FILTER MENU")
    elif add_valid_power_supply_answer["add_power_supply_selector"] == f"{CYAN}SORT":
        os.system('clear')
        print("SORT MENU")
        handle_power_supply_sort(cli_computer, valid_power_supply_names)
    elif add_valid_power_supply_answer["add_power_supply_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
        os.system('clear')
        main_menu_cli()
    elif add_valid_power_supply_answer["add_power_supply_selector"] == f"{YELLOW}RETURN TO ADD PART MENU":
        os.system('clear')
        add_part_option_cli(cli_computer)
    else:
        part_name = add_valid_power_supply_answer["add_power_supply_selector"]
        handle_add_power_supply_cli(cli_computer, part_name)

def handle_add_power_supply_cli(cli_computer, part_name):
    power_supply = find_part_by_name("power_supply", part_name)
    part_details = power_supply.display_details()
    print("DETAILS:")
    for part_type, part in part_details.items():
        print(f"{part_type}: {part}")
    handle_add_power_supply_questions = [
                inquirer.Confirm('confirm_add_power_supply', message=f'Add {power_supply.name} to {cli_computer.name}?')
            ]
    handle_add_power_supply_answers = inquirer.prompt(handle_add_power_supply_questions)
    if handle_add_power_supply_answers['confirm_add_power_supply']:
        # print(f"{cli_computer.id}, 'power_supply', {power_supply.id}")
        add_to_computer(cli_computer.id, "power_supply", power_supply.id)
        print(f'{power_supply.name} has been added to {cli_computer.name}!')
        click.echo(f'Press any button to retrun to {cli_computer.name} options.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        view_computer_options_cli(cli_computer)
    else:
        os.system('clear')
        add_part_power_supply_cli(cli_computer)

def handle_power_supply_sort(cli_computer, list):
    handle_power_supply_sort_qusetion = [
            inquirer.List(
            "power_supply_sort",
            message="FILTER BY:",
            choices=[
                "Alphabetical Ascending",
                "Alphabetical Descending",
                f"{YELLOW}BACK TO RESULTS"
            ]
            )
        ]
    handle_power_supply_sort_answers = inquirer.prompt(handle_power_supply_sort_qusetion)
    if handle_power_supply_sort_answers["power_supply_sort"] == "Alphabetical Ascending":
        sorted_list = sorted(list)
        os.system('clear')
        add_part_power_supply_cli(cli_computer, sorted_list)
    elif handle_power_supply_sort_answers["power_supply_sort"] == "Alphabetical Descending":
        sorted_list = sorted(list, reverse=True)
        os.system('clear')
        add_part_power_supply_cli(cli_computer, sorted_list)
    elif handle_power_supply_sort_answers["power_supply_sort"] == f"{YELLOW}BACK TO RESULTS":
        os.system('clear')
        add_part_power_supply_cli(cli_computer, list)
    else:
        os.system('clear')
        add_part_power_supply_cli(cli_computer, list)


#CASE ADD/////////////////////////////////////////////////////////////////////////////////////

def add_part_case_cli(cli_computer, list=[]):
    print(f"{title_add_case}")
    if len(list) is 0:
        valid_case_names = [case.name for case in valid_case(cli_computer.id)]
    else:
        valid_case_names = list
    add_valid_case_options = [
        f"{GREEN}FILTER",
        f"{CYAN}SORT",
        f"{YELLOW}RETURN TO MAIN MENU",
        f"{YELLOW}RETURN TO ADD PART MENU"
    ]
    
    add_valid_case_options.extend(valid_case_names)

    add_valid_case_qusetion = [
            inquirer.List(
            "add_case_selector",
            message="SELECT PART YOU WOULD LIKE TO SEE DETAILS OF OR WHERE YOU WOULD LIKE TO NAVIGATE",
            choices=add_valid_case_options
            )
        ]
    add_valid_case_answer = inquirer.prompt(add_valid_case_qusetion)
    if add_valid_case_answer["add_case_selector"] == f"{GREEN}FILTER":
        os.system('clear')
        print("FILTER MENU")
        handle_case_filter(cli_computer)
    elif add_valid_case_answer["add_case_selector"] == f"{CYAN}SORT":
        os.system('clear')
        print("SORT MENU")
        handle_case_sort(cli_computer, valid_case_names)
    elif add_valid_case_answer["add_case_selector"] == f"{YELLOW}RETURN TO MAIN MENU":
        os.system('clear')
        main_menu_cli()
    elif add_valid_case_answer["add_case_selector"] == f"{YELLOW}RETURN TO ADD PART MENU":
        os.system('clear')
        add_part_option_cli(cli_computer)
    else:
        part_name = add_valid_case_answer["add_case_selector"]
        handle_add_case_cli(cli_computer, part_name)

def handle_add_case_cli(cli_computer, part_name):
    case = find_part_by_name("case", part_name)
    part_details = case.display_details()
    print("DETAILS:")
    for part_type, part in part_details.items():
        print(f"{part_type}: {part}")
    handle_add_case_questions = [
                inquirer.Confirm('confirm_add_case', message=f'Add {case.name} to {cli_computer.name}?')
            ]
    handle_add_case_answers = inquirer.prompt(handle_add_case_questions)
    if handle_add_case_answers['confirm_add_case']:
        # print(f"{cli_computer.id}, 'case', {case.id}")
        add_to_computer(cli_computer.id, "case", case.id)
        print(f'{case.name} has been added to {cli_computer.name}!')
        click.echo(f'Press any button to retrun to {cli_computer.name} options.')
        c = click.getchar()
        click.echo()
        os.system('clear')
        view_computer_options_cli(cli_computer)
    else:
        os.system('clear')
        add_part_case_cli(cli_computer)

def handle_case_sort(cli_computer, list):
    handle_case_sort_qusetion = [
            inquirer.List(
            "case_sort",
            message="FILTER BY:",
            choices=[
                "Alphabetical Ascending",
                "Alphabetical Descending",
                f"{YELLOW}BACK TO RESULTS"
            ]
            )
        ]
    handle_case_sort_answers = inquirer.prompt(handle_case_sort_qusetion)
    if handle_case_sort_answers["case_sort"] == "Alphabetical Ascending":
        sorted_list = sorted(list)
        os.system('clear')
        add_part_case_cli(cli_computer, sorted_list)
    elif handle_case_sort_answers["case_sort"] == "Alphabetical Descending":
        sorted_list = sorted(list, reverse=True)
        os.system('clear')
        add_part_case_cli(cli_computer, sorted_list)
    elif handle_case_sort_answers["case_sort"] == f"{YELLOW}BACK TO RESULTS":
        os.system('clear')
        add_part_case_cli(cli_computer, list)
    else:
        os.system('clear')
        add_part_case_cli(cli_computer, list)

def handle_case_filter(cli_computer):
    valid_list = valid_case(cli_computer.id)
    handle_case_filter_qusetion = [
            inquirer.Checkbox(
            "case_filter",
            message="SELECT PART YOU WOULD LIKE TO SEE DETAILS OF OR WHERE YOU WOULD LIKE TO NAVIGATE",
            choices=[
                "Type",
                "Color",
                "Largest Motherboard Form Factor",
                "Largest Power Supply Form Factor",
                "Price",
                f"{RED}CLEAR FILTERS"
            ]
            )
        ]
    handle_case_filter_answers = inquirer.prompt(handle_case_filter_qusetion)
    new_valid_list = valid_list
    if len(handle_case_filter_answers["case_filter"]) == 0:
        new_valid_list = [case.name for case in valid_list]
    else:
        for filter in handle_case_filter_answers["case_filter"]:
            if filter == "Type":
                handle_type_filter_qusetion = [
                    inquirer.Checkbox(
                    "type_filter",
                    message="SELECT THE TYPE(S)",
                    choices=[
                        "ATX Full Tower",
                        "ATX Mid Tower",
                        "MicroATX Mid Tower",
                        "Mini ITX Desktop"
                    ]
                    )
                ]
                handle_type_filter_answers = inquirer.prompt(handle_type_filter_qusetion)
                new_valid_list = [case.name for case in new_valid_list if case.type in handle_type_filter_answers["type_filter"]]
            elif filter == "Color":
                handle_color_filter_qusetion = [
                    inquirer.Checkbox(
                    "color_filter",
                    message="SELECT THE COLOR(S)",
                    choices=[
                        "Black",
                        "White",
                        "Silver",
                    ]
                    )
                ]
                handle_color_filter_answers = inquirer.prompt(handle_color_filter_qusetion)
                new_valid_list = [case.name for case in new_valid_list if case.color in handle_color_filter_answers["color_filter"]]
            elif filter == "Largest Motherboard Form Factor":
                handle_mff_filter_qusetion = [
                    inquirer.List(
                    "mff_filter",
                    message="SELECT THE LARGEST COMPATABLE MOTHERBOARD FORM FACTOR",
                    choices=[
                    'ATX',
                    'Micro ATX',
                    'Mini ITX'
                    ]
                    )
                ]
                handle_mff_filter_answers = inquirer.prompt(handle_mff_filter_qusetion)
                form_factor_hierarchy = ['Mini ITX', 'Micro ATX', 'ATX']
                filtered_ffs = form_factor_hierarchy[form_factor_hierarchy.index(handle_mff_filter_answers["mff_filter"]):]
                new_valid_list = [case.name for case in new_valid_list if case.l_motherboard_ff in filtered_ffs]
            elif filter == "Largest Power Supply Form Factor":
                handle_psff_filter_qusetion = [
                    inquirer.List(
                    "psff_filter",
                    message="SELECT THE LARGEST COMPATABLE POWER SUPPLY FORM FACTOR",
                    choices=[
                    'ATX',
                    'SFX'
                    ]
                    )
                ]
                handle_psff_filter_answers = inquirer.prompt(handle_psff_filter_qusetion)
                form_factor_hierarchy = ['SFX', 'ATX']
                filtered_ffs = form_factor_hierarchy[form_factor_hierarchy.index(handle_psff_filter_answers["psff_filter"]):]
                new_valid_list = [case.name for case in new_valid_list if case.l_ps_ff in filtered_ffs]
            elif filter == "Price":
                while True:
                    try:
                        handle_price_floor_qusetion = [inquirer.Text("price_floor", message="SELECT THE MINIMUM PRICE",)]
                        handle_price_floor_answers = inquirer.prompt(handle_price_floor_qusetion)
                        price_floor = int(handle_price_floor_answers["price_floor"])

                        handle_price_ceiling_qusetion = [inquirer.Text("price_ceiling", message="SELECT THE MAXIMUM PRICE",)]
                        handle_price_ceiling_answers = inquirer.prompt(handle_price_ceiling_qusetion)
                        price_ceiling = int(handle_price_ceiling_answers["price_ceiling"])

                        if price_floor > price_ceiling:
                            print("The minimum price cannot be greater than the maximum price. Please enter valid values.")
                            continue

                        new_valid_list = [case.name for case in new_valid_list if price_floor < case.price < price_ceiling]
                        break
                    except ValueError:
                        print("Please enter a valid integer for price.")
            elif filter == f"{RED}CLEAR FILTERS":
                new_valid_list = [case.name for case in valid_list]
            else:
                new_valid_list = [case.name for case in valid_list]
    os.system("clear")
    add_part_case_cli(cli_computer, new_valid_list)
    








if __name__ == '__main__':
    welcome_cli()