### Constants ###
SCORE_ROWS = [2, 3, 5]
SCORE_LINK = 5
### Constants ###

### GridAnalyzer ###
class GridAnalyzer():
	def __init__(self):
		self.state = [
			[False, False, False, False, False, False, False, False, False],
			[False, False, False, False, False, False, False, False, False],
			[False, False, False, False, False, False, False, False, False]
		]

	def update_state(self, state):
		self.state = state

	def get_best_node(self):
		best_node = [0, 0]
		best_points = 0

		for i in range(len(self.state)):
			for j in range(len(self.state[i])):
				if self.state[i][j]:
					continue

				points = SCORE_ROWS[i]

				link_counted = False

				if j <= 6:
					if self.state[i][j + 1] and self.state[i][j + 2]:
						next_to_link = False

						if j <= 5 and self.state[i][j + 3]:
							next_to_link = True

						if not next_to_link:
							points += SCORE_LINK

				if not link_counted and j >= 1:
					if self.state[i][j - 1] and self.state[i][j + 1]:
						next_to_link = False

						if j >= 2 and self.state[i][j - 2]:
							next_to_link = True

						if j <= 6 and self.state[i][j + 2]:
							next_to_link = True

						if not next_to_link:
							points += SCORE_LINK

				if not link_counted and j >= 2:
					if self.state[i][j - 2] and self.state[i][j - 1]:
						next_to_link = False

						if j >= 3 and self.state[i][j - 3]:
							next_to_link = True

						if not next_to_link:
							points += SCORE_LINK

				if points > best_points:
					best_node = [i, j]
					best_points = points


		return best_node
### GridAnalyzer ###