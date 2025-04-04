Gera um programa usando QT y python,
- O programa abre uma janela com uma toolbar no topo.
    * Um toolitem "about" que al presionar faz print("about")
    * Um toolitem "Coffee" que al presionar faz print("Buy me a coffee")
    * Um toolitem "Configure" que al presionar faz print("Configure")
- abaixo da toolbar, no lado esquedo da janela se tem um treeview.
    * o treeview tem uma arvore com a seguinte estructura 
    {
        "comparison":
        {
            "bar-chart":
            {
                "vertical":   ["vbar1", "vbar2"],
                "horizontal": ["vbar1", "vbar2"],
                "clustered":  ["cbar1", "cbar2"],
                "stacked":    ["ebar1", "ebar2"]
            },
            "radar-diagram":  ["rdiag1","rdiag2"],
            "bubble-chart":   ["bchart1","bchart2"]
        },
        "distribution":
        {
            "histogram": ["hist1","hist2"],
            "boxplot":   ["boxp1","boxp2"],
            "violin":    ["viol1","viol2"]
        },
        "composition":
        {
            "piechart":     ["piechart1","piechart2"],
            "stacked-area": ["sarea1","sarea2"],
            "treemap":      ["treemap1","treemap2"]
        },
        "relation":
        {
            "scatter-plot":     ["scatter1","scatter2"],
            "correlation-plot": ["corr1","corr2"],
            "network-diagram":  ["net1","net2"]
        },
        "process":
        {
            "flowchart": ["flowchart1","flowchart2"],
            "gantt":     ["gantt1","gantt2"],
            "bpmn":      ["bpmn1","bpmn2"]
        }, 
        "strategy":
        {
            "swot":   ["swot1","swot2"],
            "bcg":    ["bcg1","bcg"],
            "ansoff": ["ansoff1","ansoff2"]
        }
    }
    quando faço click num nó me sale un print de todas as folhas finais abaixo desse nó.
    * Na direita se tem um QTabWidget com dois tabs.
        - O primeiro tab tem um QGridLayout mostrando N imagenes pequenas (usa um for desde uma lista de imagens de exemplo). Ao fazer click duplo numa imagem se executa um print com o nome da imagem.
        - O segundo tab tem um widget para mostrar uma imagem (grande coloca scroll), um text edit com scroll e tres botoes, com os textos "consult", "download image", "download code".
        - abaixo se tem um progressbar e eum status bar.
