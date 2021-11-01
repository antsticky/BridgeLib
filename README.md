# Quantitative Bridge Library

With this package one can analyze his/her play in the **Hungarian Championship** or where the same online commentation is used. This tool provides analyzer where the achieved score and playing can be compared to the field result, or to the theoretical optimum ([double dummy](https://www.nytimes.com/2005/01/29/crosswords/bridge/how-double-dummy-started-and-a-question-it-could-raise.html)).

The `project/base` folder contains all the necessary libraries which need for a basic play with seating, bidding, and playing a pre-defined or randomly shuffered board. The `project/analytics` provides an interface with the online commentator program and containes a double dummy solver.

:warning: **Do not** forgot to build the DDS package before use it, for installation steps reach the [manual](https://github.com/antsticky/BridgeLib/tree/main/project/analytics/dds_project)

## Examples
For this repository a few examples are attached, see [Examples](https://github.com/antsticky/BridgeLib/tree/main/examples).


## External Links
-  **Bo Haglund**'s and **Soren Hein**'s double dummy solver - [C++ implementation](https://github.com/dds-bridge/dds)
- **Foppe Hemminga**'s python interface for the double dummy solver -[Python Interface](https://github.com/Afwas/python-dds)
- How 'Double Dummy' Started, and a Question It Could Raise - [NYTimes article](https://www.nytimes.com/2005/01/29/crosswords/bridge/how-double-dummy-started-and-a-question-it-could-raise.html)
