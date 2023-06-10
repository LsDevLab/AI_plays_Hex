

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="images/logo.png" alt="Logo" width="100" height="100">

  <h2 align="center">AI plays Hex</h2>

  <h4 align="center">Final project for Intelligent Agents course at Unisa DIEM</h2>

  <p align="center">
    A Python project to explore game search, heuristics and other techniques to play Hex
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Read the paper</strong></a>
    <br />
    <br />
  </p>
</div>


## How to run

The file main.py contains a GUI to play with the available AIs or to see different AIs playing

All you need to do is to setup game config

```python
    board_size = 11
    config = {
        'board_size': board_size,
        'AI_vs_AI': True,
        'max_depth': 2,
        'AI1_node_value_heuristic': heuristics.TwoDistanceValueHeuristic(),
        'AI1_node_ordering_heuristic': heuristics.ChargeHeuristic(board_size),
        'AI2_node_value_heuristic': heuristics.ShortestPathValueHeuristic(),
        'AI2_node_ordering_heuristic': heuristics.RandomOrderHeuristic(),
        'starting_player': -1
    }
   ```

and run the python script.

<!-- ROADMAP -->
## Roadmap

- [x] Alpha-beta pruning search
- [x] Develop some node value heuristics
- [x] Develop some node ordering heuristics
- [ ] Optimize search with other techniques


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


