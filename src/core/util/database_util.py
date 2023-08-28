from sqlalchemy.orm import Session


def domain_save(domain, db: Session):
    db.add(domain)
    db.flush()
    db.refresh(domain)
    return domain


def domain_all_save(domain_list: list, db: Session):
    db.add_all(domain_list)
    db.flush()
    return domain_list


def like_search(str_val):
    return "%" + str(str_val) + "%"