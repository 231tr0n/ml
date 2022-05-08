print()
print("Snaketron")
print()
import os
import time
import random
import json
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
module_availability = True
try:
	import pygame
except:
	print("pygame module is not available on your computer")
	module_availability = False
if module_availability:
	import pygame
	pygame.init()
	replay = True
	temp_snake_head = ()
	present_state_string = ""
	present_q_value = 0
	gamma = 0
	alpha = 1
	snake_left = (0, -1)
	snake_right = (0, 1)
	snake_down = (1, 0)
	snake_up = (-1, 0)
	red = (213, 0, 0)
	blue = (0, 0, 255)
	green = (0, 255, 9)
	black = (0, 0, 0)
	yellow = (255, 255, 0)
	snake_head = ()
	snake_food = ()
	snake_body_coordinates = []
	game_count = 0
	with open("dataset.json", "r") as file_data:
		q_table = json.load(file_data)
		file_data.close()
	def add_coordinates(coordinates_1, coordinates_2):
		x_coordinate = coordinates_1[0] + coordinates_2[0]
		y_coordinate = coordinates_1[1] + coordinates_2[1]
		coordinates = (x_coordinate, y_coordinate)
		return coordinates
	def state_string_cell_finder(state_string):
		state_values = {}
		for i in q_table["dataset"]:
			if (i["state"] == state_string):
				state_values = i
				break
		return state_values
	def state_string_cell_index_finder(state_string):
		state_values = {}
		x = 0
		for i in q_table["dataset"]:
			if (i["state"] == state_string):
				break
			else:
				x = x + 1
		return x
	def state_string_getter():
		s = "|" + str(snake_head[0]) + "," + str(snake_head[1]) + "|"
		s = s + str(snake_food[0]) + "," + str(snake_food[1]) + "|"
		return s
	def q_table_cell_generator():
		q_table["information"][0]["total_dataset_cells_count"] = q_table["information"][0]["total_dataset_cells_count"] + 1
		s = state_string_getter()
		json_data = {
			"state" : s,
			"left" : 0,
			"right" : 0,
			"up" : 0,
			"down" : 0
		}
		q_table["dataset"].append(json_data)
	def reward_generator():
		temp_snake_head = add_coordinates(snake_head, snake_direction)
		temp_distance = abs(temp_snake_head[0] - snake_food[0]) + abs(temp_snake_head[1] - snake_food[1])
		distance = abs(snake_head[0] - snake_food[0]) + abs(snake_head[1] - snake_food[1])
		if (temp_snake_head[0] == 0 or temp_snake_head[0] == (display_height - 1) or temp_snake_head[1] == 0 or temp_snake_head[1] == (display_width - 1)):
			return (-2)
		elif (temp_snake_head == snake_food):
			return 1
		elif (temp_snake_head in snake_body_coordinates):
			return (-2)
		else:
			if (temp_distance > distance):
				return (-0.6)
			else:
				return 0.1
	def q_table_value_updater():
		s = state_string_getter()
		state_string_cell = state_string_cell_finder(s)
		if (state_string_cell != {}):
			if (snake_direction == snake_left):
				maximum_next_state_value = max(state_string_cell["left"], state_string_cell["up"], state_string_cell["down"])
			elif (snake_direction == snake_right):
				maximum_next_state_value = max(state_string_cell["right"], state_string_cell["up"], state_string_cell["down"])
			elif (snake_direction == snake_up):
				maximum_next_state_value = max(state_string_cell["right"], state_string_cell["up"], state_string_cell["left"])
			elif (snake_direction == snake_down):
				maximum_next_state_value = max(state_string_cell["right"], state_string_cell["left"], state_string_cell["down"])
		else:
			q_table_cell_generator()
			maximum_next_state_value = 0
		present_state_string_index = state_string_cell_index_finder(present_state_string)
		if (snake_direction == snake_left):
			present_q_value = q_table["dataset"][present_state_string_index]["left"]
			q_table["dataset"][present_state_string_index]["left"] = round((present_q_value + alpha * (reward + (gamma * maximum_next_state_value) - present_q_value)), 5)
		elif (snake_direction == snake_right):
			present_q_value = q_table["dataset"][present_state_string_index]["right"]
			q_table["dataset"][present_state_string_index]["right"] = round((present_q_value + alpha * (reward + (gamma * maximum_next_state_value) - present_q_value)), 5)
		elif (snake_direction == snake_up):
			present_q_value = q_table["dataset"][present_state_string_index]["up"]
			q_table["dataset"][present_state_string_index]["up"] = round((present_q_value + alpha * (reward + (gamma * maximum_next_state_value) - present_q_value)), 5)
		elif (snake_direction == snake_down):
			present_q_value = q_table["dataset"][present_state_string_index]["down"]
			q_table["dataset"][present_state_string_index]["down"] = round((present_q_value + alpha * (reward + (gamma * maximum_next_state_value) - present_q_value)), 5)
	def alpha_updater():
		global alpha
		alpha = 1
	def gamma_updater():
		global gamma
		gamma = 0.1
	while replay:
		if (game_count == 0):
			snake_speed = float(input("Enter the time after which the snake should move one unit(speed of the snake) else enter '0' for default value: "))
			pixel_size = int(input("Enter the size of each pixel else enter '0' for default value: "))
			if (pixel_size == 0):
				pixel_size = 30
			display_width = 10
			display_height = 10
		alpha_updater()
		gamma_updater()
		game_count = game_count + 1
		food_eaten = True
		game_over = False
		game_finished = False
		game_score = 0
		snake_direction = snake_right
		snake_body_coordinates = []
		display_window = pygame.display.set_mode((display_width * pixel_size, display_height * pixel_size))
		pygame.display.set_caption("Snaketron | Score: " + str(game_score))
		if (display_height % 2 == 0):
			temporary_variable = display_height / 2
			snake_head = (int(temporary_variable) - 1, 1)
		else:
			temporary_variable = (display_height + 1) / 2
			snake_head = (int(temporary_variable) - 1, 1)
		coordinates_list = []
		for i in range(1, display_height - 1):
			for j in range(1, display_width - 1):
				coordinates_list = coordinates_list + [(i, j)]
		for i in range(display_height):
			for j in range(display_width):
				if (i == 0 or i == (display_height - 1) or j == 0 or j == (display_width - 1)):
					matrix_element = 1
				elif (i == snake_head[0] and j == snake_head[1]):
					matrix_element = 4
				else:
					matrix_element = 0
				if (matrix_element == 0):
					pygame.draw.rect(display_window, black, [j * pixel_size, i * pixel_size, pixel_size, pixel_size])
				elif (matrix_element == 1):
					if (pixel_size >= 15):
						pygame.draw.rect(display_window, red, [j * pixel_size, i * pixel_size, pixel_size, pixel_size])
						pygame.draw.rect(display_window, black, [(j * pixel_size) + 1, (i * pixel_size) + 1, pixel_size - 2, pixel_size - 2])
						pygame.draw.rect(display_window, red, [(j * pixel_size) + 4, (i * pixel_size) + 4, pixel_size - 8, pixel_size - 8])
					else:
						pygame.draw.rect(display_window, black, [j * pixel_size, i * pixel_size, pixel_size, pixel_size])
						pygame.draw.rect(display_window, red, [(j * pixel_size) + 2, (i * pixel_size) + 2, pixel_size - 4, pixel_size - 4])
				elif (matrix_element == 4):
					if (pixel_size >= 15):
						pygame.draw.rect(display_window, blue, [j * pixel_size, i * pixel_size, pixel_size, pixel_size])
						pygame.draw.rect(display_window, black, [(j * pixel_size) + 1, (i * pixel_size) + 1, pixel_size - 2, pixel_size - 2])
						pygame.draw.rect(display_window, blue, [(j * pixel_size) + 4, (i * pixel_size) + 4, pixel_size - 8, pixel_size - 8])
					else:
						pygame.draw.rect(display_window, black, [j * pixel_size, i * pixel_size, pixel_size, pixel_size])
						pygame.draw.rect(display_window, blue, [(j * pixel_size) + 2, (i * pixel_size) + 2, pixel_size - 4, pixel_size - 4])
		pygame.display.update()
		while not game_over:
			if food_eaten:
				temporary_coordinates_list = coordinates_list.copy()
				temporary_list = [snake_head] + snake_body_coordinates
				for j in temporary_list:
					if j in temporary_coordinates_list:
						temporary_coordinates_list.remove(j)
				if (len(temporary_coordinates_list) == 0):
					game_over = True
					game_finished = True
					break
				snake_food = random.choice(temporary_coordinates_list)
				food_eaten = False
				if (pixel_size >= 15):
					pygame.draw.rect(display_window, green, [snake_food[1] * pixel_size, snake_food[0] * pixel_size, pixel_size, pixel_size])
					pygame.draw.rect(display_window, black, [(snake_food[1] * pixel_size) + 1, (snake_food[0] * pixel_size) + 1, pixel_size - 2, pixel_size - 2])
					pygame.draw.rect(display_window, green, [(snake_food[1] * pixel_size) + 4, (snake_food[0] * pixel_size) + 4, pixel_size - 8, pixel_size - 8])
				else:
					pygame.draw.rect(display_window, black, [snake_food[1] * pixel_size, snake_food[0] * pixel_size, pixel_size, pixel_size])
					pygame.draw.rect(display_window, green, [(snake_food[1] * pixel_size) + 2, (snake_food[0] * pixel_size) + 2, pixel_size - 4, pixel_size - 4])
				pygame.display.update()
			present_state_string = state_string_getter()
			present_state_string_cell = state_string_cell_finder(present_state_string)
			if (present_state_string_cell == {}):
				q_table_cell_generator()
				present_q_value = 0
				if (snake_direction == snake_left):
					temp_action_list = ["left", "up", "down"]
				elif (snake_direction == snake_right):
					temp_action_list = ["right", "up" , "down"]
				elif (snake_direction == snake_up):
					temp_action_list = ["left", "right", "up"]
				elif (snake_direction == snake_down):
					temp_action_list = ["left", "right", "down"]
				for i in temp_action_list:
					if (i == "left"):
						temp_snake_head = add_coordinates(snake_head, snake_left)
						if (temp_snake_head[0] == 0 or temp_snake_head[0] == (display_height - 1) or temp_snake_head[1] == 0 or temp_snake_head[1] == (display_width - 1)):
							if (len(temp_action_list) > 1):
								temp_action_list.remove("left")
					if (i == "right"):
						temp_snake_head = add_coordinates(snake_head, snake_right)
						if (temp_snake_head[0] == 0 or temp_snake_head[0] == (display_height - 1) or temp_snake_head[1] == 0 or temp_snake_head[1] == (display_width - 1)):
							if (len(temp_action_list) > 1):
								temp_action_list.remove("right")
					if (i == "up"):
						temp_snake_head = add_coordinates(snake_head, snake_up)
						if (temp_snake_head[0] == 0 or temp_snake_head[0] == (display_height - 1) or temp_snake_head[1] == 0 or temp_snake_head[1] == (display_width - 1)):
							if (len(temp_action_list) > 1):
								temp_action_list.remove("up")
					if (i == "down"):
						temp_snake_head = add_coordinates(snake_head, snake_down)
						if (temp_snake_head[0] == 0 or temp_snake_head[0] == (display_height - 1) or temp_snake_head[1] == 0 or temp_snake_head[1] == (display_width - 1)):
							if (len(temp_action_list) > 1):
								temp_action_list.remove("down")
				action_index = random.choice(temp_action_list)
			else:
				if (snake_direction == snake_left):
					temp_action_list = {"left" : present_state_string_cell["left"], "up" : present_state_string_cell["up"], "down" : present_state_string_cell["down"]}
				elif (snake_direction == snake_right):
					temp_action_list = {"right" : present_state_string_cell["right"], "up" : present_state_string_cell["up"], "down" : present_state_string_cell["down"]}
				elif (snake_direction == snake_up):
					temp_action_list = {"left" : present_state_string_cell["left"], "right" : present_state_string_cell["right"], "up" : present_state_string_cell["up"]}
				elif (snake_direction == snake_down):
					temp_action_list = {"left" : present_state_string_cell["left"], "right" : present_state_string_cell["right"], "down" : present_state_string_cell["down"]}
				present_q_value = max(temp_action_list.values())
				action_index = max(temp_action_list, key = temp_action_list.get)
			if (action_index == "left"):
				if (snake_direction != snake_right and snake_direction != snake_left):
					snake_direction = snake_left
			elif (action_index == "right"):
				if (snake_direction != snake_left and snake_direction != snake_right):
					snake_direction = snake_right
			elif (action_index == "up"):
				if (snake_direction != snake_down and snake_direction != snake_up):
					snake_direction = snake_up
			elif (action_index == "down"):
				if (snake_direction != snake_up and snake_direction != snake_down):
					snake_direction = snake_down
			reward = reward_generator()
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					game_over = True
				else:
					keys = pygame.key.get_pressed()
					if (keys[pygame.K_SPACE]):
						pause = True
						pygame.display.set_caption("Snaketron | Score: " + str(game_score) + " | Paused")
						while pause:
							for event in pygame.event.get():
								if (event.type == pygame.QUIT):
									game_over = True
								else:
									keys = pygame.key.get_pressed()
									if (keys[pygame.K_SPACE]):
										pygame.display.set_caption("Snaketron | Score: " + str(game_score))
										pause = False
					elif (keys[pygame.K_q]):
						q_table["information"][0]["snake_games_count"] = q_table["information"][0]["snake_games_count"] + game_count
						with open("dataset.json", "w") as file_data:
							json.dump(q_table, file_data, indent = 4)
						file_data.close()
						game_over = True
						replay = False
						pygame.quit()
						break
			temp_snake_head = snake_head
			snake_body_coordinates = [temp_snake_head] + snake_body_coordinates
			snake_head = add_coordinates(snake_head, snake_direction)
			if (snake_head == snake_food):
				food_eaten = True
				game_score = game_score + 1
				pygame.display.set_caption("Snaketron | Score: " + str(game_score))
				pygame.draw.rect(display_window, black, [snake_food[1] * pixel_size, snake_food[0] * pixel_size, pixel_size, pixel_size])
				pygame.display.update()
			if not food_eaten:
				resetted_coordinates = snake_body_coordinates.pop()
				if (snake_head[0] == 0 or snake_head[0] == (display_height - 1) or snake_head[1] == 0 or snake_head[1] == (display_width - 1) or snake_head in snake_body_coordinates):
					game_over = True
					if (q_table["information"][0]["highest_score"] < game_score):
						q_table["information"][0]["highest_score"] = game_score;
				else:
					game_over = False
			q_table_value_updater()
			temporary_list = [snake_head, temp_snake_head]
			if not food_eaten:
				temporary_list = temporary_list + [resetted_coordinates]
			for k in temporary_list:
				if (k == snake_head):
					matrix_element = 4
				elif (k == resetted_coordinates):
					matrix_element = 0
				else:
					matrix_element = 3
				if (matrix_element == 0):
					pygame.draw.rect(display_window, black, [k[1] * pixel_size, k[0] * pixel_size, pixel_size, pixel_size])
				elif (matrix_element == 3):
					if (pixel_size >= 15):
						pygame.draw.rect(display_window, yellow, [k[1] * pixel_size, k[0] * pixel_size, pixel_size, pixel_size])
						pygame.draw.rect(display_window, black, [(k[1] * pixel_size) + 1, (k[0] * pixel_size) + 1, pixel_size - 2, pixel_size - 2])
						pygame.draw.rect(display_window, yellow, [(k[1] * pixel_size) + 4, (k[0] * pixel_size) + 4, pixel_size - 8, pixel_size - 8])
					else:
						pygame.draw.rect(display_window, black, [k[1] * pixel_size, k[0] * pixel_size, pixel_size, pixel_size])
						pygame.draw.rect(display_window, yellow, [(k[1] * pixel_size) + 2, (k[0] * pixel_size) + 2, pixel_size - 4, pixel_size - 4])
				elif (matrix_element == 4):
					if (pixel_size >= 15):
						pygame.draw.rect(display_window, blue, [k[1] * pixel_size, k[0] * pixel_size, pixel_size, pixel_size])
						pygame.draw.rect(display_window, black, [(k[1] * pixel_size) + 1, (k[0] * pixel_size) + 1, pixel_size - 2, pixel_size - 2])
						pygame.draw.rect(display_window, blue, [(k[1] * pixel_size) + 4, (k[0] * pixel_size) + 4, pixel_size - 8, pixel_size - 8])
					else:
						pygame.draw.rect(display_window, black, [k[1] * pixel_size, k[0] * pixel_size, pixel_size, pixel_size])
						pygame.draw.rect(display_window, blue, [(k[1] * pixel_size) + 2, (k[0] * pixel_size) + 2, pixel_size - 4, pixel_size - 4])
			pygame.display.update()
			time.sleep(snake_speed)
