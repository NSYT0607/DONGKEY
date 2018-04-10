from django import template

register = template.Library()


def won(value):
    """숫자를 원화로 변경"""
    if value >= 0:
        value = str(value)
        length = len(value)
        new_val_list = []
        if length <= 3:
            new_val_list.append(value[0:length])
        else:
            if length % 3 == 0:
                for n in range(1, (length//3)+1):
                    new_val_list.append(value[(n-1)*3:n*3])
            elif length % 3 == 1:
                new_val_list.append(value[0:1])
                for n in range(1, (length//3)+1):
                    new_val_list.append(value[(n*3)-2:(n+1)*3-2])
            else:
                new_val_list.append(value[0:2])
                for n in range(1, (length//3)+1):
                    new_val_list.append(value[n*3-1:(n+1)*3-1])

        value = ','.join(new_val_list)
        value = value + '원'
        return value
    else:
        value = str(value)[1:]
        length = len(value)
        new_val_list = []
        if length <= 3:
            new_val_list.append(value[0:length])
        else:
            if length % 3 == 0:
                for n in range(1, (length//3)+1):
                    new_val_list.append(value[(n-1)*3:n*3])
            elif length % 3 == 1:
                new_val_list.append(value[0:1])
                for n in range(1, (length//3)+1):
                    new_val_list.append(value[(n*3)-2:(n+1)*3-2])
            else:
                new_val_list.append(value[0:2])
                for n in range(1, (length//3)+1):
                    new_val_list.append(value[n*3-1:(n+1)*3-1])

        value = ','.join(new_val_list)
        value = '-' + value + '원'
        return value


register.filter('won', won)




