import math
import pygame
import random
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorith Visualization")
        self.set_list(lst)
        self.animation_speed = 1
        self.comparison_count = 0

    def set_animation_speed(self, speed):
        self.animation_speed = max(1, min(speed, 10))
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2
    def increment_comparison_count(self):
        self.comparison_count += 1
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    title_rect = title.get_rect(center=(draw_info.width/2, 20))
    draw_info.window.blit(title, title_rect)

    controls = draw_info.FONT.render("R - reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    controls_rect = controls.get_rect(center=(draw_info.width/2, 60))
    draw_info.window.blit(controls, controls_rect)

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort | Q - Quick Sort", 1, draw_info.BLACK)
    sorting_rect = sorting.get_rect(center=(draw_info.width/2, 90))
    draw_info.window.blit(sorting, sorting_rect)

    draw_list(draw_info)
    comparison_text = draw_info.FONT.render(f"Comparison Count: {draw_info.comparison_count}", 1, draw_info.BLACK)
    comparison_text_rect = comparison_text.get_rect(center=(draw_info.width / 2, 140))
    draw_info.window.blit(comparison_text, comparison_text_rect)
    pygame.display.update()

    animation_speed = draw_info.FONT.render(f"Animation Speed: {draw_info.animation_speed} FPS", 1, draw_info.BLACK)
    animation_speed_rect = animation_speed.get_rect(center=(draw_info.width / 2, 115))
    draw_info.window.blit(animation_speed, animation_speed_rect)

    wait_time = max(5, round(50 / draw_info.animation_speed))
    pygame.time.wait(wait_time)

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_react = (
            draw_info.SIDE_PAD // 2,
            draw_info.TOP_PAD,
            draw_info.width - draw_info.SIDE_PAD,
            draw_info.height - draw_info.TOP_PAD,
        )
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_react)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

        text = draw_info.FONT.render(str(val), 1, draw_info.BLACK, draw_info.BACKGROUND_COLOR)
        small_font = pygame.font.SysFont('comicsans', 12)
        small_text = small_font.render(str(val), 1, draw_info.BLACK)
        text_rect = small_text.get_rect(center=(x + draw_info.block_width // 2, draw_info.height - 10))
        draw_info.window.blit(small_text, text_rect)

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range (n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    draw_info.comparison_count = 0

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                draw_info.comparison_count += 1
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
                wait_time = max(5, round(10 / draw_info.animation_speed))
                pygame.time.wait(wait_time)
    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    draw_info.comparison_count = 0

    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_info.comparison_count += 1
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
            wait_time = max(5, round(10 / draw_info.animation_speed))
            pygame.time.wait(wait_time)
    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    draw_info.comparison_count = 0

    for i in range(len(lst)):
        min_idx = i

        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                draw_info.comparison_count += 1
                min_idx = j

        (lst[i], lst[min_idx]) = (lst[min_idx], lst[i])
        draw_list(draw_info, {min_idx: draw_info.GREEN, i: draw_info.RED}, True)
        yield True
        wait_time = max(5, round(10 / draw_info.animation_speed))
        pygame.time.wait(wait_time)
    return lst


def partition(draw_info,arr, low, high, ascending=True):
    i = low - 1
    pivot = arr[high]

    for j in range(low, high):
        draw_info.comparison_count += 1
        if (arr[j] <= pivot and ascending) or (arr[j] >= pivot and not ascending):
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(draw_info, arr, low, high, ascending=True):
    if low < high:
        pivot_index = partition(draw_info, arr, low, high, ascending)
        quick_sort(draw_info, arr, low, pivot_index - 1, ascending)
        quick_sort(draw_info, arr, pivot_index + 1, high, ascending)
        wait_time = max(5, round(10 / draw_info.animation_speed))
        pygame.time.wait(wait_time)

def merge(draw_info, arr, left, mid, right, ascending=True):
    n1 = mid - left + 1
    n2 = right - mid

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[left + i]

    for j in range(n2):
        R[j] = arr[mid + 1 + j]

    i = j = 0
    k = left

    while i < n1 and j < n2:
        draw_info.comparison_count += 1
        if (L[i] <= R[j] and ascending) or (L[i] >= R[j] and not ascending):
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def merge_sort(draw_info, arr, left, right, ascending=True):
    if left < right:
        mid = (left + right) // 2
        merge_sort(draw_info, arr, left, mid, ascending)
        merge_sort(draw_info, arr, mid + 1, right, ascending)
        merge(draw_info, arr, left, mid, right, ascending)
        wait_time = max(5, round(10 / draw_info.animation_speed))
        pygame.time.wait(wait_time)


def draw_input_screen():
    width = 700
    height = 400

    input_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Sorting Algorithm Input")

    font = pygame.font.SysFont('comicsans', 30)
    text = font.render("Liste boyutunu giriniz ve giriş tuşuna basınız:", 1, DrawInformation.BLACK)
    text_rect = text.get_rect(center=(width / 2, height / 2 - 20))

    input_value = ""
    is_typing = True

    while is_typing:
        input_window.fill(DrawInformation.BACKGROUND_COLOR)
        input_window.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_typing = False
                elif event.key == pygame.K_BACKSPACE:
                    input_value = input_value[:-1]
                else:
                    input_value += event.unicode

        input_text = font.render(input_value, 1, DrawInformation.BLACK)
        input_text_rect = input_text.get_rect(center=(width / 2, height / 2 + 20))
        input_window.blit(input_text, input_text_rect)
        pygame.display.update()

    return int(input_value)
def create_input_window(width, height):
    input_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("List Input")
    return input_window
def draw_input_button(draw_info):
    button_font = pygame.font.SysFont('comicsans', 20)
    button_text = button_font.render("Enter List", 1, draw_info.BLACK)
    button_rect = button_text.get_rect(center=(draw_info.width/2, draw_info.height-50))

    draw_info.window.blit(button_text, button_rect)

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    if button_rect.collidepoint(mouse_pos):
        if mouse_clicked:
            open_list_input_window(draw_info)

def open_list_input_window(draw_info):
    input_width = 500
    input_height = 200
    input_window = create_input_window(input_width, input_height)

    input_value = ""
    is_typing = True

    while is_typing:
        input_window.fill(draw_info.BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_typing = False
                elif event.key == pygame.K_BACKSPACE:
                    input_value = input_value[:-1]
                else:
                    input_value += event.unicode

        input_font = pygame.font.SysFont('comicsans', 30)
        input_text = input_font.render(input_value, 1, draw_info.BLACK)
        input_text_rect = input_text.get_rect(center=(input_width / 2, input_height / 2))
        input_window.blit(input_text, input_text_rect)
        pygame.display.update()

    # Girdileri işleyerek yeni bir liste oluşturun
    new_list = [int(num) for num in input_value.split()]
    draw_info.set_list(new_list)

def main():
    run = True
    clock = pygame.time.Clock()
    size = draw_input_screen()
    n = size
    min_val = 0
    max_val = 500
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1500, 800, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(2*draw_info.animation_speed)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
            pygame.display.update()
            clock.tick(draw_info.animation_speed)

        if pygame.time.get_ticks() % 100 == 0:
            draw_info.comparison_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not sorting:
                        draw_info.animation_speed += 1
                        draw_info.set_animation_speed(draw_info.animation_speed)
                elif event.key == pygame.K_DOWN:
                    if not sorting:
                        draw_info.animation_speed -= 1
                        draw_info.set_animation_speed(draw_info.animation_speed)



            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_m and not sorting:
                draw_info.comparison_count = 0
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
                lst_copy = list(draw_info.lst)
                if ascending == True:
                    merge_sort(draw_info, lst_copy, 0, len(lst_copy) - 1, ascending=True)
                else:
                    merge_sort(draw_info, lst_copy, 0, len(lst_copy) - 1, ascending=False)
                draw_info.set_list(lst_copy)
            elif event.key == pygame.K_q and not sorting:
                draw_info.comparison_count = 0
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
                lst_copy = list(draw_info.lst)
                if ascending == True:
                    quick_sort(draw_info, lst_copy, 0, len(lst_copy) - 1, ascending=True)
                else:
                    quick_sort(draw_info, lst_copy, 0, len(lst_copy) - 1, ascending=False)
                draw_info.set_list(lst_copy)

    pygame.quit()

if __name__ == "__main__":
    main()