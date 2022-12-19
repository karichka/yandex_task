import pandas as pd

df = pd.read_excel(r'Yandex_task/models.xlsx')

total_cars = df['car_cnt'].sum()
total_brand_cars = df['car_sticker_cnt'].sum()
total_not_brand_cars = total_cars - total_brand_cars

print(f'Всего машин в сервисе: {total_cars}')
print(f'Всего брендированных машин в сервисе: {total_brand_cars}')
print(f'Всего не брендированных машин в сервисе: {total_not_brand_cars}' + '\n')

model_car_count = df[(df['can_be_branded'] == True) & (df['car_sticker_cnt'] != 0)]['trips_success_cnt'].sum()

average_ride = df.groupby(['model']).agg(
    {'car_cnt': 'sum', 'car_sticker_cnt': 'sum', 'trips_success_cnt': 'sum', 'trips_cancel_cnt': 'sum'})


average_ride = average_ride.assign(branding_rate = lambda x: x.car_sticker_cnt / x.car_cnt * 100)
average_ride = average_ride.assign(average_ride_rate = lambda x: x.trips_success_cnt / x.car_cnt)
success_trips_total = average_ride['trips_success_cnt'].sum()

average_rate = average_ride['average_ride_rate'].mean()
average_hibrand_rate = average_ride[(average_ride['branding_rate'] >= 50)]['average_ride_rate'].mean()
average_lowbrand_rate = average_ride[(average_ride['branding_rate'] < 50)]['average_ride_rate'].mean()
grow_potential = average_hibrand_rate / average_lowbrand_rate - 1
potential_trips_not_branded = (average_rate * total_not_brand_cars) * (1 + grow_potential)

print(average_ride)

print(f'Среднее кол-во успешных поездок на брендированной машине: {round(average_hibrand_rate, 2)}')
print(f'Среднее кол-во успешных поездок на не брендированной машине: {round(average_lowbrand_rate, 2)}')
print(f'Потенциал роста кол-ва успешных поездок на одну машину при полной оклейке автопарка: {round(grow_potential, 2)} %' + '\n')
print(f'Относительный потенциал роста кол-ва успешных поездок при полной оклейке автопарка: {round(potential_trips_not_branded / success_trips_total - 1, 2)} %')
