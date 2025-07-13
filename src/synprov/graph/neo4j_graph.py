class Node:
    def __init__(self, n_labels, properties):
        self.labels = n_labels if isinstance(n_labels, list) else [n_labels]
        self.properties = properties

    def __getitem__(self, key):
        return self.properties[key]

    def items(self):
        return self.properties.items()

    def to_dict(self):
        return {**{'labels': self.labels}, **self.properties}

    def __repr__(self):
        return f"Node(labels={self.labels}, properties={self.properties})"


class Neo4jGraph:
    def __init__(self, driver):
        self.driver = driver

    def run(self, query, **parameters):
        with self.driver.session() as session:
            result = session.run(query, **parameters)
            return result.data()
        
    def nodes(self, label=None, **properties):
        with self.driver.session() as session:
            if label:
                query = f"MATCH (n:{label})"
            else:
                query = "MATCH (n)"
            if properties:
                query += " WHERE " + " AND ".join([f"n.{k} = ${k}" for k in properties.keys()])
            query += " RETURN n"
            result = session.run(query, **properties)
            return [record['n'] for record in result]
        

    def relationships(self, start_label=None, end_label=None, **properties):
        with self.driver.session() as session:
            query = "MATCH (s)-[r]->(e)"
            if start_label:
                query += f" WHERE s:{start_label}"
            if end_label:
                query += f" AND e:{end_label}"
            if properties:
                query += " AND " + " AND ".join([f"r.{k} = ${k}" for k in properties.keys()])
            query += " RETURN r"
            result = session.run(query, **properties)
            return [record['r'] for record in result]


    def nodes_match(self, label, **properties):
        with self.driver.session() as session:
            query = f"MATCH (n:{label} {{"
            query += ", ".join([f"{k}: ${k}" for k in properties.keys()])
            query += "}) RETURN n"
            result = session.run(query, **properties)
            return result.single()

    def merge(self, node):
        with self.driver.session() as session:
            query = f"MERGE (n:{node.labels[0]} {{id: $id}}) SET n += $properties RETURN n"
            properties = {k: v for k, v in node.items() if k != 'id'}
            result = session.run(query, id=node['id'], properties=properties)
            return result.single()

    def delete_all(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            session.run("CALL db.clearQueryCaches()")

    def close(self):
        self.driver.close()