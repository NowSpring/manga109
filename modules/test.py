import xml.etree.ElementTree as ET

# XMLデータの例
xml_data = '''
<root>
    <elementA index="10">ValueA</elementA>
    <elementB index="25">ValueB</elementB>
    <elementC index="5">ValueC</elementC>
</root>
'''

# XMLデータをElementTreeに変換
root = ET.fromstring(xml_data)

# indexが25の要素を抽出
target_index = "10"
desired_element = next((elem for elem in root if elem.get("index") == target_index), None)

# 結果を表示
if desired_element is not None:
    print(f"Desired Element: {desired_element.tag}, Index: {desired_element.get('index')}, Text: {desired_element.text}")
else:
    print(f"No element with index {target_index} found.")

print(int(8.8))