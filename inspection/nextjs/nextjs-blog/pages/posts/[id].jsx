import Layout from "../../components/Layout";

import { getAllPostIds } from "../../lib/posts";

export async function getStaticPaths() {
  const paths = getAllPostIds();
  return {
    paths,
    fallback: false,
  };
}

export default function Post() {
  return (
    <Layout>
      <h1>Post</h1>
    </Layout>
  );
}
