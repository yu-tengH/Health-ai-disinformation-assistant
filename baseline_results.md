
1.
mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --prompt "什麼是計畫行為理論？"
arning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads. | 0/7 [00:00<?, ?it/s]
Fetching 7 files: 100%|██████████████████████████| 7/7 [01:16<00:00, 10.98s/it]
Download complete: : ██████████████████████████████████████| 1.48GB, 11.2MB/s  
Reconstruction complete: 100%|████████████████████| 1.49GB / 1.49GB, 24.3MB/s  
==========
計畫行為理論 (Planned Behavior Theory)  是一種  **行為的理論模型**  ，旨在  **解釋人們的行為模式**  。  它基於  **三項核心因素**:  

* **  動機  **:  人們的行為動機  
* **  自我效能  **:  人們對自己的能力  
* **  環境  **:  環境的影響  

  計畫行為理論  強調  **人們的行為是由於他們對行為的
==========
Prompt: 15 tokens, 11.206 tokens-per-sec
Generation: 100 tokens, 69.733 tokens-per-sec
Peak memory: 1.523 GB

1-1(20iters, 2batch)
(venv) tenghuang@Tengs-MacBook-Air ollma_thesis %  mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --adapter-path ./adapters_iter20 --prompt "什麼是計 畫行為理論？" --max-tokens 300
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2508.77it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
計畫行為理論（Theory of Planned Behavior，TPB）提出，人們的行為決定力主要取決於主觀規範（主觀規範的影響力遠大於社會規範），而非行為的實際可行性。也就是說，人們更常被自己的價值觀和主觀規範所驅動，而不是社會規範的直接影響力。
==========
Prompt: 15 tokens, 87.525 tokens-per-sec
Generation: 79 tokens, 57.410 tokens-per-sec
Peak memory: 1.567 GB


2.
mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --prompt "什麼是計畫行為理論中的主觀規範？"
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2410.52it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
在計畫行為理論中，主觀規範指的是人們根據自己的價值觀、經驗和期望來制定計畫的過程。  

簡單來說，它指的是：

* **個人經驗和價值觀:**  人們的計畫行為受個人經驗和價值觀的影響。例如，一個喜歡挑戰的個人可能會制定更具挑戰性的計畫，而一個注重安全的人則可能會制定更安全計畫。
* **期望和目標:**  人們制定計畫時，會根據自己的
==========
Prompt: 20 tokens, 35.649 tokens-per-sec
Generation: 100 tokens, 70.509 tokens-per-sec
Peak memory: 1.532 GB

1-2(20iters, 2batch)
(venv) tenghuang@Tengs-MacBook-Air ollma_thesis %  mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --adapter-path ./adapters_iter20 --prompt "什麼是計 畫行為理論？" --max-tokens 300
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2508.77it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
計畫行為理論（Theory of Planned Behavior，TPB）提出，人們的行為決定力主要取決於主觀規範（主觀規範的影響力遠大於社會規範），而非行為的實際可行性。也就是說，人們更常被自己的價值觀和主觀規範所驅動，而不是社會規範的直接影響力。
==========
Prompt: 15 tokens, 87.525 tokens-per-sec
Generation: 79 tokens, 57.410 tokens-per-sec
Peak memory: 1.567 GB
(venv) tenghuang@Tengs-MacBook-Air ollma_thesis % mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --adapter-path ./adapters_iter20 --prompt "什麼是計畫行為理論中的主觀規範？" --max-tokens 300
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2656.54it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
主觀規範（Subjective Norms）指的是一個人對他人的觀感（如親友、社群、典範人物）的影響力。它是一種「我應該怎麼做」的推力，而非單純的道德規範。
==========
Prompt: 20 tokens, 117.210 tokens-per-sec
Generation: 54 tokens, 60.749 tokens-per-sec
Peak memory: 1.585 GB


3.
mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --prompt "AI標籤能不能有效幫助使用者辨識AI生成的健康資訊？"
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2194.33it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
AI標籤的有效性與使用者辨識AI生成的健康資訊的程度存在著挑戰。以下是一些分析：

**利點:**

* **提高意識:**  標籤能讓使用者意識到資訊來源，並提醒他們資訊可能存在偏差或不完整。
* **資訊來源可追溯:**  標籤可讓使用者了解資訊來源的類型和內容，例如 AI 模型的訓練數據、生成模型的設計等等。
* **驗證資訊
==========
Prompt: 23 tokens, 137.893 tokens-per-sec
Generation: 100 tokens, 72.800 tokens-per-sec
Peak memory: 1.536 GB

1-3(20iters, 2batch)
(venv) tenghuang@Tengs-MacBook-Air ollma_thesis % mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --adapter-path ./adapters_iter20 --prompt "AI標籤能不能有效幫助使用者辨識AI生成的健康資訊？" --max-tokens 600
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2883.25it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
根據我的研究，AI標籤並不能有效幫助使用者辨識AI生成的健康資訊。這主要是因為：
==========
Prompt: 23 tokens, 110.134 tokens-per-sec
Generation: 24 tokens, 58.955 tokens-per-sec
Peak memory: 1.595 GB


4.
mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --prompt "網傳蘋果山楂茶可以瘦身美白降三高，這則訊息可信嗎？"
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2683.99it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
這則訊息需要多角度考量，以下提供一些資訊和分析：

**關於山楂茶的功效:**

* **山楂:**  山楂含有豐富的維生素、礦物質和多酚類化合物，這些成分可能具有一定的抗氧化、抗炎和降血脂功效。
* **瘦身:**  山楂茶的功效可能與其含有的酸性物質和多酚類化合物有关。  但需要注意的是，山楂茶並
==========
Prompt: 31 tokens, 174.843 tokens-per-sec
Generation: 100 tokens, 73.772 tokens-per-sec
Peak memory: 1.573 GB

1-4(20iters, 2batch)
(venv) tenghuang@Tengs-MacBook-Air ollma_thesis % mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --adapter-path ./adapters_iter20 --prompt "AI標籤能不能有效幫助使用者辨識AI生成的健康資訊？" --max-tokens 600
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2883.25it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
根據我的研究，AI標籤並不能有效幫助使用者辨識AI生成的健康資訊。這主要是因為：
==========
Prompt: 23 tokens, 110.134 tokens-per-sec
Generation: 24 tokens, 58.955 tokens-per-sec
Peak memory: 1.595 GB
(venv) tenghuang@Tengs-MacBook-Air ollma_thesis % mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --adapter-path ./adapters_iter20 --prompt "網傳蘋果山楂茶可以瘦身美白降三高，這則訊息可信嗎？" --max-tokens 300
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2334.80it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
根據我查證，這則訊息並非出自正當的健康機構或研究社群。它主要利用了「山楂」這類常見的健康食材，加上「瘦身、美白、降三高」這類容易被認可的健康標籤，製造出讓人容易被動化的訊息。
==========
Prompt: 31 tokens, 170.866 tokens-per-sec
Generation: 69 tokens, 60.383 tokens-per-sec
Peak memory: 1.636 GB
(venv) tenghuang@Tengs-MacBook-Air ollma_thesis % 








測試一：
(venv) tenghuang@Tengs-MacBook-Air ollma_thesis % mlx_lm.lora \
  --model mlx-community/gemma-2-2b-it-4bit \
  --train \
  --data ./data \
  --iters 100 \
  --batch-size 2 \
  --adapter-path ./adapters
Loading pretrained model
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2879.57it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
Loading datasets
Training
Trainable parameters: 0.244% (6.390M/2614.342M)
Starting training..., iters: 100
Calculating loss...: 100%|███████████████████████| 2/2 [00:01<00:00,  1.46it/s]
Iter 1: Val loss 5.941, Val took 1.427s
Iter 10: Train loss 4.444, Learning Rate 1.000e-05, It/sec 0.744, Tokens/sec 162.806, Trained Tokens 2187, Peak mem 4.241 GB
Iter 20: Train loss 2.324, Learning Rate 1.000e-05, It/sec 1.236, Tokens/sec 270.327, Trained Tokens 4374, Peak mem 4.394 GB
Iter 30: Train loss 1.158, Learning Rate 1.000e-05, It/sec 1.210, Tokens/sec 264.557, Trained Tokens 6561, Peak mem 4.394 GB
Iter 40: Train loss 0.463, Learning Rate 1.000e-05, It/sec 1.190, Tokens/sec 260.333, Trained Tokens 8748, Peak mem 4.394 GB
Iter 50: Train loss 0.205, Learning Rate 1.000e-05, It/sec 1.180, Tokens/sec 258.098, Trained Tokens 10935, Peak mem 4.394 GB
Iter 60: Train loss 0.119, Learning Rate 1.000e-05, It/sec 1.212, Tokens/sec 265.035, Trained Tokens 13122, Peak mem 4.394 GB
Iter 70: Train loss 0.066, Learning Rate 1.000e-05, It/sec 1.269, Tokens/sec 277.561, Trained Tokens 15309, Peak mem 4.394 GB
Iter 80: Train loss 0.049, Learning Rate 1.000e-05, It/sec 1.254, Tokens/sec 274.198, Trained Tokens 17496, Peak mem 4.394 GB
Iter 90: Train loss 0.044, Learning Rate 1.000e-05, It/sec 1.259, Tokens/sec 275.364, Trained Tokens 19683, Peak mem 4.394 GB
Calculating loss...: 100%|███████████████████████| 2/2 [00:00<00:00,  3.96it/s]
Iter 100: Val loss 4.067, Val took 0.509s
Iter 100: Train loss 0.042, Learning Rate 1.000e-05, It/sec 1.262, Tokens/sec 275.934, Trained Tokens 21870, Peak mem 4.394 GB
Iter 100: Saved adapter weights to adapters/adapters.safetensors and adapters/0000100_adapters.safetensors.
Saved final weights to adapters/adapters.safetensors.
(venv) tenghuang@Tengs-MacBook-Air ollma_thesis % mlx_lm.generate --model mlx-community/gemma-2-2b-it-4bit --adapter-path ./adapters --prompt "什麼是計畫行為理 論中的主觀規範？" --max-tokens 300
Fetching 7 files: 100%|████████████████████████| 7/7 [00:00<00:00, 2917.92it/s]
Reconstruction complete: |                        |  0.00B /  0.00B            
Download complete: :                                       |  0.00B            
==========
主觀規範（Subjective Norms）在計畫行為理論中，指的是**一個人對他人或社會 norma 的真實感受，以及他/她認為這代表了什麼**。例如，一個人可能覺得「如果媽媽知道我沒有提醒她，一定會生氣」，這代表了他/她對母親愛與批評的真實感受，也代表了他/她認為母親重視他/她的態度，而不是他的提醒行為本身。
==========
Prompt: 20 tokens, 31.873 tokens-per-sec
Generation: 92 tokens, 61.641 tokens-per-sec
Peak memory: 1.579 GB


