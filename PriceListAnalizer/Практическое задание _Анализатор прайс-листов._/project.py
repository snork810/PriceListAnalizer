import glob
import os
import pandas as pd


class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0
        self.df = pd.DataFrame()  # Инициализация пустого DataFrame

    def load_prices(self,
                    file_path='F:\PYTHON\pyton_progects\PriceListAnalizer\Практическое задание _Анализатор прайс-листов._'):
        csv_files = glob.glob(os.path.join(file_path, '*price*.csv'))
        df_list = []

        for file in csv_files:
            df = pd.read_csv(file)
            df.rename(columns={
                'товар': 'Названия',
                'название': 'Названия',
                'наименование': 'Названия',
                'продукт': 'Названия',
                'розница': 'Цена',
                'цена': 'Цена',
                'вес': 'Вес(кг)',
                'масса': 'Вес(кг)',
                'фасовка': 'Вес(кг)'
            }, inplace=True)
            df_list.append(df)

        combined_df = pd.concat(df_list, ignore_index=True)
        combined_df = combined_df[['Названия', 'Цена', 'Вес(кг)']]
        sorted_df = combined_df.sort_values(by='Цена')  # Сортировка по столбцу 'Цена'

        self.df = sorted_df  # Сохранение DataFrame в self.df
        return self.df

    def export_to_html(self, df, search_query):
        """
        Экспортирует результаты поиска в HTML файл.
        """
        html_string = df.to_html(index=False, escape=False)

        # Создание полного HTML-документа
        full_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Результаты поиска: {search_query}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>Результаты поиска для "{search_query}"</h1>
            {html_string}
        </body>
        </html>
        '''

        output_file = f"search_results_{search_query}.html".replace(" ", "_")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"Результаты записаны в файл: {output_file}")

    def search_product(self, fragment):
        if self.df.empty:
            return pd.DataFrame()  # Возвращаем пустой DataFrame, если нет данных

        result = self.df[self.df['Названия'].str.contains(fragment, case=False, na=False)]
        result['Цена за кг'] = (result['Цена'] / result['Вес(кг)']).round(2)
        sorted_result = result.sort_values(by='Цена за кг')

        return sorted_result[['Названия', 'Цена', 'Вес(кг)', 'Цена за кг']]

    def run_search_interface(self):
        print("Введите фрагмент названия для поиска товара. Введите 'exit' для выхода.")
        while True:
            query = input("Поиск: ")
            if query.lower() == 'exit':
                print("Выход из программы.")
                break

            search_result = self.search_product(query)
            if search_result.empty:
                print("Товары не найдены.")
            else:
                print(search_result)
                self.export_to_html(search_result, query)


# Использование класса
pm = PriceMachine()
pm.load_prices()
pm.run_search_interface()