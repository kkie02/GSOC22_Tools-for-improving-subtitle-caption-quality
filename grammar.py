from happytransformer import TTTrainArgs, HappyTextToText, HappyGeneration, TTSettings
import re

def rm_punca(text):
    punctuation = f",.¿?!@#$%^&*)(':+<>/÷" + '"-'
    text = re.sub(r"[%s]+" %punctuation,' ',text)
    return text.strip()

if __name__ == '__main__':
    happy_gen = HappyTextToText(model_type="google/mt5-base",     model_name="JorgeSarry/est5base", load_path=".grammar/model/")
    beam_settings =  TTSettings(num_beams=5, min_length=1, max_length=40)
    # Start to set parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str)
    args = parser.parse_args()

    print(f'Start to load file {args.file}')
    file_path = args.file
    ip_file = open(file_path, 'r')
    lines = ip_file.readlines()
    for line in lines:
        if line.split('|')[-2] not in ['CC1','CCO']:
          continue
        else:
          words = line.split('|')[-1]
          words = words.strip()
          words = words.strip("\n")
          pred = happy_gen.generate_text(words.strip(), args=beam_settings)
        orig_in = words.lower()
        pred_res = pred.text.lower()

        orig_in = rm_punca(words)
        pred_res = rm_punca(pred.text)
        if orig_in==pred_res:
          continue
        elif orig_in in pred_res:
          continue
        else:
          print("Possible wrong sentences:")
          print(f"Orig: {words}")
          print(f"Corr: {pred.text}")