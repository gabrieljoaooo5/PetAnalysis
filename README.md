# PetAnalysis

O objetivo deste ciclo é continuar o desenvolvimento de uma aplição que automatiza o processo de análise de marcha com o uso de **dois Kinects** simultaneamente.

## Motivação

Esta aplicação é visada para ser aplicada em clínicas de fisioterapia, dado que no Brasil, tipicamente, clínicas convencionais não têm muito espaço físico e carecem de recursos financeiros para adquirir ferramentas de ponta para fazer a análise de marcha automatizada. Por isso, são forçados a realizarem o processo de forma análogica, o que é um trabalho laboroso que pode ser melhorado em termos de precisão e quantidade de *features* obtidas.

Uma gravação utiliza um espaço no qual o paciente.

1. inicia a marcha,
2. prossegue com a marcha,
3. desacelera para o final da marcha.

Os passos 1 e 3 são descartados para uma análise menos tendenciosa, dado que nessas fases o paciente está acelerando ou desacelerado, o que não configura como uma marcha natural. Por isso, métodos de gravação com câmeras costumam apontá-las para a área que é mais ou menos o centro do local de passada. Para facilitar, a gravação, pretendemos usar dois Kinects para **aumentar o _range_ de gravação últil**.

## Trabalho já realizado

### Setup

Para conseguir fazer uma gravação com mais de uma câmera, é essencial a **sincronização** delas. Como não se pode usar dois Kinects num mesmo computador, o método usa **dois computadores**, cada um resposável por obter as informações de um Kinect conectado. Na indústria de captura de vídeo com múltiplas câmeras, normalmente uma câmera **mestre** grava seu video ao mesmo tempo que recebe a os vídeos das outras câmeras, chamadas de **escravas**.

Com dois vídeos sincronizados, o temos dois **skeletons** sincronizados, mas diferentes. Para avaliar os dados, é necessário unir (**interpolar**) estes dois skeletons em um só. Espera-se que este skeleton produto da soma seja mais preciso e consiga se manter consistente ao longo de todo o percurso útil da marcha.

### Resultados

## Objetivo